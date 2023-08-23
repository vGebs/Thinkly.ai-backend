from flask import request, Blueprint
from helpers import create_chat_model_prompt, parse_response_content
import json
from billing import pushUsage
from datetime import datetime

# Create a Blueprint instance
bp = Blueprint("assignmentCreation", __name__)


@bp.route("/assignment/makeAssignment", methods=["POST"])
def getAssignment():
    data = request.get_json()
    subunit = data.get("subunit")
    uid = data.get("uid")

    if not uid:
        print("Failure: uid is empty.")
        return {"error": "Failure: uid is empty"}, 422

    prompt = f"""
        Given this unit: {subunit},
        
        Generate an assignment consisting of 5 questions that cover the material from the unit and make sure each question gets more challenging.
        
        Output in the following JSON format:
        {{"questions": [String]}}
        
        Begin every question with the (index + 1), for example question 1 will start like this: "1. ....."
        
        Do not respond to this message, simply output the JSON object.
    """

    response = create_chat_model_prompt(prompt)
    usage = response["usage"]
    usage["uid"] = uid
    usage["timestamp"] = datetime.now()

    pushUsage(usage)

    content_dict = parse_response_content(response)

    return content_dict, 200


# Generate a single question given existing questions
@bp.route("/assignment/makeQuestion", methods=["POST"])
def makeQuestion():
    data = request.get_json()

    questions = data.get("questions")
    outline = data.get("weeklyOutline")
    assignment = data.get("assignment")
    difficulty = data.get("difficultyLevelOutOfTen")

    prompt = f"""
        Given this assignment: 
        
        {assignment},
        
        these existing questions:
        
        {questions},
        
        and this outline:
        
        {outline},
        
        Generate one question with {difficulty}/10 difficulty and output in this JSON format:
        
        {{"question": String, "difficultyLevelOutOfTen": Int}}
        
        Do not respond to this message, simply output the JSON object.
    """

    response = create_chat_model_prompt(prompt)

    # Parsing and cleaning up the content
    content_dict = parse_response_content(response)

    return content_dict, 200


# Write this question in more depth
@bp.route("/assignment/addDepthToQuestion", methods=["POST"])
def addDepthToQuestion():
    question = request.get_json()

    prompt = f"""
        Given this question:
        
        "{question}".
        
        Write this question in more depth.
        
        Ouput in this JSON format:
        
        {{"question": String, "difficultyLevelOutOfTen": Int}}
        
        Do not respond to this message, simply out the the JSON object.
    """

    response = create_chat_model_prompt(prompt)

    # Parsing and cleaning up the content
    content_dict = parse_response_content(response)

    return content_dict, 200


@bp.route("/assignment/chatAboutAssignmentQuestion", methods=["post"])
def askQuestionAboutAssignment():
    data = request.get_json()
    chat = data.get("chat")
    assignment = data.get("assignmentProblem")
    textbooks = data.get("courseTextbooks")

    prompt = f"""
        Given this student's question/ the current gpt chat:
        
        {chat},
        
        the assignment problem itself:
        
        {assignment},
        
        and the reading material for this course:
        
        {textbooks},
        
        Address their question and provide a brief answer to their question and then provide them with 
        specific books and chapters /resources to read regarding their question. I also want you to 
        give them encouragement and show them empathy but do not be condescending.
        
        Output your response in this JSON format:
        
        {{"assignmentProblem": String, "studentQuestion": String, gptResponse: String}}
        
        If the student asks the assignment problem (or have reworded the assignment problem), do not give them a direct answer.
        
        Do not respond to this message, simply output the JSON object.
    """

    response = create_chat_model_prompt(prompt)

    # Parsing and cleaning up the content
    content_dict = parse_response_content(response)

    return content_dict, 200
