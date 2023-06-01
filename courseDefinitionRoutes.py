from flask import request, Blueprint
from helpers import create_chat_model_prompt, parse_response_content, remove_newlines
import json

# Create a Blueprint instance
bp = Blueprint("courseDefinition", __name__)


@bp.route("/findTextbookOverlap", methods=["POST"])
def findTextbookOverlap():
    textbooks = request.get_json()

    prompt = f"""
        Given these textbooks:
        {textbooks}
        List the overlapping ideas between them and order them in order of precedence.

        Output this information in this JSON format:

        {{ "concepts": [{{"conceptTitle": String, "descriptionOfConcept": String, "overlapRatingOutOfTen": Int}}]}}
        
        Only include the overlap if the rating is greater than 5.
        
        Do not respond to this message, simply output in JSON.
    """

    response = create_chat_model_prompt(prompt)

    # Parsing and cleaning up the content
    content_dict = parse_response_content(response)
    content_dict_no_newlines = remove_newlines(content_dict)

    return content_dict_no_newlines, 200


@bp.route("/getLearningObjectives", methods=["POST"])
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
    content_dict_no_newlines = remove_newlines(content_dict)

    return content_dict_no_newlines, 200


@bp.route("/getPrerequisites", methods=["POST"])
def getPrerequisites():
    return 200


@bp.route("/getCourseTitleSuggestion", methods=["POST"])
def getCourseTitleSuggestion():
    return 200
