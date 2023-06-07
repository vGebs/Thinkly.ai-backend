from flask import request, Blueprint
from helpers import create_chat_model_prompt, parse_response_content
import json

# Create a Blueprint instance
bp = Blueprint("noteQuestions", __name__)


@bp.route("/noteQuestions/askQuestion", methods=["POST"])
def askQuestion():
    data = request.get_json()

    convo = data.get("convo")

    if wasRelevant(convo):
        return answerQuestion(convo)
    else:
        return {
            "error": "Kindly maintain focus on the subject at hand. Pose inquiries that are pertinent to the ongoing topic."
        }, 200


def wasRelevant(convo):
    prompt = f"""
    
        Is the most recent message from 'user' relevant to the conversation?
        
        convo: {convo}.
        
        If so, answer it and do not mention whether it was relevant. 
        
        {{"wasRelevant": Bool}}
        
        Do not respond to this message, simply output the JSON object whether it was relevant or not, do not comment on the question.
    """

    response = create_chat_model_prompt(prompt)

    # Parsing and cleaning up the content
    content_dict = parse_response_content(response)

    if content_dict["wasRelevant"] == True:
        return True
    else:
        return False


def answerQuestion(convo):
    prompt = f"""
    
        Given this conversation:
        {convo},
        
        respond to the users most recent query.
        
        Output in this JSON format: 
        
        {{"response": String}}.
        
        Do not respond to this message at all, simply output the JSON object.
    """

    response = create_chat_model_prompt(prompt)

    # Parsing and cleaning up the content
    content_dict = parse_response_content(response)

    return content_dict, 200
