from flask import request, Blueprint
from helpers import create_chat_model_prompt, parse_response_content, remove_newlines
import json

# Create a Blueprint instance
bp = Blueprint("assignmentCreation", __name__)


@bp.route("/makeAssignment", methods=["POST"])
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
    content_dict_no_newlines = remove_newlines(content_dict)

    return content_dict_no_newlines, 200
