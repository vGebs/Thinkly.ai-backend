from flask import request, Blueprint
from helpers import create_chat_model_prompt, parse_response_content
import json

# Create a Blueprint instance
bp = Blueprint("quizCreation", __name__)


@bp.route("/generateQuiz", methods=["POST"])
def generateQuiz():
    data = request.get_json()

    prompt = f"""
        Given this outline:
        
        {data}
        
        Generate a quiz consisting of multiple choice as well as true or false.
        
        Output in this JSON format:
        
        quiz: [{{"question": String, "possibleAnswers": [String], "correctAnswer": String, "questionType": String}}]
        
        For questionType, the correct outputs are: MultipleChoice, TrueOrFalse
        
        Do not reply to this message, simply output the JSON object.
    """

    response = create_chat_model_prompt(prompt)

    # Parsing and cleaning up the content
    content_dict = parse_response_content(response)

    return content_dict, 200


@bp.route("/generateQuizQuestion", methods=["POST"])
def generateQuizQuestion():
    data = request.get_json()

    quizParams = data.get("quizParameters")
    questions = data.get("existingQuestions")
    outline = data.get("weeklyOutline")
    difficulty = data.get("difficultyLevelOutOfTen")

    prompt = f"""
        Given these quiz parameters: 
        
        {quizParams},
        
        these existing questions:
        
        {questions},
        
        and this outline:
        
        {outline},
        
        Generate one question with {difficulty}/10 difficulty and output in this JSON format:
        
        {{"question": String, "possibleAnswers": [String], "correctAnswer": String, "questionType": String}}
        
        Do not respond to this message, simply output the JSON object.
    """

    response = create_chat_model_prompt(prompt)

    # Parsing and cleaning up the content
    content_dict = parse_response_content(response)

    return content_dict, 200


@bp.route("/addDepthToQuizQuestion", methods=["POST"])
def addDepthToQuizQuestion():
    data = request.get_json()
    question = data.get("question")
    prompt = f"""
        Given this question:
        
        "{question}".
        
        And the whole question outline:
        
        {data},
        
        Write this question in more depth.
        
        Ouput in this JSON format:
        
        {{"question": String, "possibleAnswers": [String], "correctAnswer": String, "questionType": String}}
        
        Do not respond to this message, simply out the the JSON object.
    """

    response = create_chat_model_prompt(prompt)

    # Parsing and cleaning up the content
    content_dict = parse_response_content(response)

    return content_dict, 200
