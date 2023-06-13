from flask import request, Blueprint
from helpers import create_chat_model_prompt, parse_response_content
import json

# Create a Blueprint instance
bp = Blueprint("courseDefinition", __name__)


@bp.route("/courseDefinition/findTextbookOverlap", methods=["POST"])
def findTextbookOverlap():
    textbooks = request.get_json()

    prompt = f"""
        Given these textbooks:
        {textbooks}
        List the overlapping ideas between them and order them in order of precedence.

        Output this information in this JSON format:

        {{ "concepts": [{{"conceptTitle": String, "descriptionOfConcept": String, "overlapRatingOutOfTen": Int}}]}}
        
        Only include the overlap if the rating is greater than 5.
        
        Do not respond to this message, simply output in JSON, do not elaborate either.
    """

    response = create_chat_model_prompt(prompt)

    # Parsing and cleaning up the content
    content_dict = parse_response_content(response)

    return content_dict, 200


@bp.route("/courseDefinition/getLearningObjectives", methods=["POST"])
def getLearningObjectives():
    concepts = request.get_json()

    prompt = f"""
        Given these concepts:
        {concepts}
        
        Create a list of learning objectives based on the concepts in this JSON format:
        
        learningObjectives: [{{"objectiveTitle": String, "description": String}}]
        
        Do not respond to this message, simply output in JSON.
    """

    response = create_chat_model_prompt(prompt)

    # Parsing and cleaning up the content
    content_dict = parse_response_content(response)

    return content_dict, 200


@bp.route("/courseDefinition/getCourseTitleSuggestion", methods=["POST"])
def getCourseTitleSuggestion():
    learningObjectives = request.get_json()

    prompt = f"""
        Given these learning objectives:
        
        {learningObjectives}
        
        Generate a list of 5 possible titles for the course with their associated description.
        
        Output in this JSON format:
        
        courseOverview: [{{"courseTitle": String, "courseDescription": String}}]
        
        Do not respond to this message, simply output in JSON.
    """

    response = create_chat_model_prompt(prompt)

    # Parsing and cleaning up the content
    content_dict = parse_response_content(response)

    return content_dict, 200


@bp.route("/courseDefinition/getPrerequisites", methods=["POST"])
def getPrerequisites():
    data = request.get_json()

    textbooks = data.get("textbooks")
    learningObjectives = data.get("learningObjectives")
    courseOverview = data.get("courseOverview")

    prompt = f"""
        Given these textbooks:
        {textbooks},
        
        These learning objectives:
        {learningObjectives},
        
        and the course overview:
        {courseOverview},
        
        Generate a list or prerequisites in this JSON format:
        
        prerequisites: [{{"prerequisiteTitle": String, "prerequisiteDescription": String}}] 
        
        Do not respond to this message, simply output in JSON.
    """

    response = create_chat_model_prompt(prompt)

    # Parsing and cleaning up the content
    content_dict = parse_response_content(response)

    return content_dict, 200
