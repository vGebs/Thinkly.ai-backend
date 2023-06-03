from flask import request, Blueprint
from helpers import create_chat_model_prompt, parse_response_content
import json

# Create a Blueprint instance
bp = Blueprint("grading", __name__)


@bp.route("/grading/generateRubric", methods=["POST"])
def generateRubric():
    data = request.get_json()
    problem = data.get("problem")
    gradeLevel = data.get("gradeLevel")
    prompt = f"""
        Assume this is a question/problem/exercise on a {gradeLevel} assignment:

        {problem}

        what do you think the scoring metrics should be?
        
        Create rubric with specific scoring metrics.

        Output in this JSON format:  
        
        "criteria": [{{"criterion_name": String, "criterion_weight_outOfTen": Int, "criterion_description_forTeacher": String, "criterion_description_forStudent": String}}]
        
        criterion_description_forTeacher should be more comprehensive, while criterion_description_forStudent should be less comprehensive (we don't want to give away the solution. We want the students to use their critical thinking skills.)
                
        Do not respond to this message, simply output the JSON object.
    """

    response = create_chat_model_prompt(prompt)

    # Parsing and cleaning up the content
    content_dict = parse_response_content(response)

    return content_dict, 200


@bp.route("/grading/gradeAnswer", methods=["POST"])
def gradeAnswer():
    data = request.get_json()

    exercise = data.get("exercise")
    studentAnswer = data.get("studentAnswer")
    rubric = data.get("rubric")
    perfectAnswer = data.get("perfectAnswer")
    gradeLevel = data.get("gradeLevel")

    prompt = f"""
        Prentend you are a teacher.
        
        Given this course assignment exercise:
        
        {exercise},
        
        the student's answer:
        
        {studentAnswer},
        
        and this grading rubric:
        
        {rubric},
        
        Grade the student's answer given that this is a {gradeLevel} course.
        
        Grade in relation to the rubric. Make sure to give feedback for the criterion.
        
        Output in this JSON format:
        
        {{"scoring": [{{"criterion_name": String, "scoreOutOfOneHundred": Int, "rationalForScore": String}}], "finalGradeBeforeScaler_outOfOneHundred": Int, "finalGradeAfterScaler_outOfOneHundred": Int}}
        
        Make sure to keep an eye out for misinformation. If there is misinformation, acknowledge it in the response.
        
        Do not respond to this message, simply output the JSON object.
    """

    response = create_chat_model_prompt(prompt)

    # Parsing and cleaning up the content
    content_dict = parse_response_content(response)

    return content_dict, 200


@bp.route("/grading/makeAppeal", methods=["POST"])
def makeAppeal():
    data = request.get_json()

    exercise = data.get("exercise")
    scoreCard = data.get("scoreCard")
    appeal = data.get("appeal")

    prompt = f"""
        You are a teacher and a student is making an appeal on a specific assignment question.
        
        Given this exercise:
        
        {exercise},
        
        this score card,
        
        {scoreCard},
        
        and the students appeal,
        
        {appeal},
        
        Provide a detailed rationale why they do or do not deserve extra grades.
        
        If the student deserves extra grades, update the score of both the scoring criterion and update the final grade accordingly.
        
        Do not allow excuses, be impartial and make sure to be fair.
        
        If they make a logical arguement on why they should receive a higher grade, go back and determine if the student deserves it.
        
        I also want you to give them encouragement and show them empathy but do not be condescending.
        
        Output your response in this JSON format:
        
        {{"rational": String, "scoreCard": {{"finalGradeBeforeScaler_outOfOneHundred": Int, "finalGradeAfterScaler_outOfOneHundred": Int, "finalGradeAfterAppeal_outOfOneHundred": String, "scoring": [{{"criterion_name": String, "rationalForScore": String, "scoreOutOfOneHundred": Int}}]}}
        
        Do not respond to this message, simply output the JSON object.
    """

    response = create_chat_model_prompt(prompt)

    # Parsing and cleaning up the content
    content_dict = parse_response_content(response)

    return content_dict, 200
