from flask import request, Blueprint
from helpers import create_chat_model_prompt, parse_response_content
import json
from billing import pushUsage
from datetime import datetime

# Create a Blueprint instance
bp = Blueprint("courseCreation", __name__)


@bp.route("/courseCreation/generateCurriculum", methods=["POST"])
def generateCurriculum():
    input = request.get_json()
    userPrompt = input.get("prompt")
    uid = input.get("uid")

    if not uid:
        print("Failure: uid is empty.")
        return {"error": "Failure: uid is empty"}, 422

    prompt = f"""
        Give this users prompt:
        {userPrompt},
        
        Generate a comprehensive curriculum for this topic.
        
        Do not include a final exam/ project/ assignments/ quizzes.
        
        Output the units in this JSON format:
        {{"units": [{{"unitTitle": String, "unitDescription": String, "unitNumber": Int}}]}}
        
        Do not respond to this message, simply output the JSON object.
    """

    response = create_chat_model_prompt(prompt)

    usage = response["usage"]
    usage["uid"] = uid
    usage["timestamp"] = datetime.now()
    pushUsage(usage)

    content_dict = parse_response_content(response)

    return content_dict, 200


@bp.route("/courseCreation/generateSubTopicsForUnit", methods=["POST"])
def generateSubTopicsForUnit():
    data = request.get_json()
    curriculum = data.get("curriculum")
    unitNumber = data.get("unitNumber")
    uid = data.get("uid")

    if not uid:
        print("Failure: uid is empty.")
        return {"error": "Failure: uid is empty"}, 422

    prompt = f"""
        Given this curriculum:
        {curriculum},
        
        Create a list of subtopics for unit number {unitNumber}. Make sure to take the other units into consideration before making the subtopics.

        output in this json format:

        {{"subUnits": [{{"unitTitle": String, "unitDescription": String, "unitNumber": Double}}]}}
        
        Do not respond to this message, simply output the JSON object.
    """
    response = create_chat_model_prompt(prompt)

    usage = response["usage"]
    usage["uid"] = uid
    usage["timestamp"] = datetime.now()

    pushUsage(usage)

    content_dict = parse_response_content(response)

    return content_dict, 200


@bp.route("/courseCreation/generateLessonsForSubunit", methods=["POST"])
def generateLessonsForSubunit():
    data = request.get_json()
    curriculum = data.get("curriculum")
    subunitNumber = data.get("subunitNumber")
    uid = data.get("uid")

    if not uid:
        print("Failure: uid is empty.")
        return {"error": "Failure: uid is empty"}, 422

    prompt = f""" 
        Given this Curriculum:
        {curriculum},
        
        Create a list of lessons for subunit number {subunitNumber}. Make sure to take the other sub units into account before making the lessons.
        
        if subunit number is 2.1, then the lesson numbers will be 2.1.1, 2.1.2, and so on.
        Furthermore, if the subunit number is 3.3, then the lesson numbers will be 3.3.1, 3.3.2, and so on.
        
        output in this json format:

        {{"lessons": [{{"lessonTitle": String, "lessonDescription": String, "lessonNumber": String}}]}}
        
        Do not respond to this message, simply output the JSON object.
    """

    response = create_chat_model_prompt(prompt)

    usage = response["usage"]
    usage["uid"] = uid
    usage["timestamp"] = datetime.now()
    pushUsage(usage)

    content_dict = parse_response_content(response)

    return content_dict, 200


@bp.route("/courseCreation/generateNotesForLesson", methods=["POST"])
def generateNotesForLesson():
    data = request.get_json()
    unit = data.get("unit")
    lessonNumber = data.get("lessonNumber")
    uid = data.get("uid")

    if not uid:
        print("Failure: uid is empty.")
        return {"error": "Failure: uid is empty"}, 422

    prompt = f""" 
        Given this unit:
        {unit},
        
        Write the notes for this lesson that the students will use to study. Write as many comprehensive paragraphs as necessary for lesson {lessonNumber}.
        The first paragraph will be the title and the rest will be the reading material.
        Make to sure to make the text engaging yet informational.
        
        Output in the following JSON format:
        
        {{"notes": [{{"paragraph": String}}]}}
        
        Ouput each paragraph in its own string.
        
        Do not respond to this message, simply output the JSON object.
    """

    response = create_chat_model_prompt(prompt)
    usage = response["usage"]
    usage["uid"] = uid
    usage["timestamp"] = datetime.now()
    pushUsage(usage)

    content_dict = parse_response_content(response)

    return content_dict, 200
