from flask import request, Blueprint
from helpers import create_chat_model_prompt, parse_response_content
import json

# Create a Blueprint instance
bp = Blueprint("assignmentCreation", __name__)


@bp.route("/assignment/makeAssignment", methods=["POST"])
def getAssignment():
    data = request.get_json()
    difficulty = data.get("difficultyOutOfTen")

    prompt = f"""
        Given this assignment description:
        
        {data},
        
        Generate an assignment.
        
        Output in the following JSON format:
        
        questions: [{{"question": String, "difficultyLevelOutOfTen": Int}}]
        
        Do not respond to this message, simply output in JSON.
    """

    response = create_chat_model_prompt(prompt)

    # Parsing and cleaning up the content
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


# Generate a comprehensive answer for this question
@bp.route("/assignment/makeAnswer", methods=["POST"])
def makeAnswer():
    question = request.get_json()

    prompt = f"""
        Given this question:
        
        {question},
        
        Provide a detailed answer that would result in full marks.
        
        Output the answer in this JSON format:
        
        {{"question": String, "answer": String}}
        
        Do not respond to this message, simply output the JSON object.
        Do not include Control characters.
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
        give them encouragement and show them empathy.
        
        Output your response in this JSON format:
        
        {{"assignmentProblem": String, "studentQuestion": String, gptResponse: String}}
        
        If the student asks the assignment problem (or have reworded the assignment problem), do not give them a direct answer.
        
        Do not respond to this message, simply output the JSON object.
    """

    response = create_chat_model_prompt(prompt)

    # Parsing and cleaning up the content
    content_dict = parse_response_content(response)

    return content_dict, 200
