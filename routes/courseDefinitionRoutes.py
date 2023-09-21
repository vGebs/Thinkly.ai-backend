from flask import request, Blueprint
from helpers import create_chat_model_prompt, parse_response_content
import json
from billing import pushUsage
from datetime import datetime

# Create a Blueprint instance
bp = Blueprint("courseDefinition", __name__)


@bp.route("/courseDefinition/getCourseTitleSuggestionFromCurriculum", methods=["POST"])
def getCourseTitleSuggestionFromCurriculum():
    input = request.get_json()
    curriculum = input.get("units")
    uid = input.get("uid")

    if not uid:
        print("Failure: uid is empty.")
        return {"error": "Failure: uid is empty"}, 422

    prompt = f"""
        Given this curriculum:
        
        {curriculum}.
        
        Generate a list of 5 possible titles for the course with their associated description.
        
        Output in this JSON format:
        
        {{"courseOverview": [{{"courseTitle": String, "courseDescription": String}}]}}
        
        Do not respond to this message, simply output in JSON format.
    """

    response = create_chat_model_prompt(prompt)
    usage = response["usage"]
    usage["uid"] = uid
    usage["timestamp"] = datetime.now()
    pushUsage(usage)
    content_dict = parse_response_content(response)

    return content_dict, 200
