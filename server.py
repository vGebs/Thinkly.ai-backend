from flask import Flask, request, jsonify

from dotenv import load_dotenv
import os
import openai
import json

# Set up OpenAI API
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)


def create_chat_model_prompt(content: str) -> dict:
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": content},
        ],
    )


def parse_response_content(response):
    content = response.choices[0].message["content"]
    return json.loads(content)


def remove_newlines(obj):
    if isinstance(obj, str):
        return obj.replace("\n", " ")
    elif isinstance(obj, list):
        return [remove_newlines(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: remove_newlines(value) for key, value in obj.items()}
    else:
        return obj


@app.route("/getWeeklyContent", methods=["POST"])
def getWeeklyContent():
    # Get the entire JSON object
    data = request.get_json()
    week = data.get("week")
    course_json = data.get("course")

    # Initial OpenAI request
    initial_prompt = f""" 
        Generate a course outline based on the following details for each week:
        {course_json}
        Please output the course outline in json defined as follows: 

        weeklyContent: [{{"week": Int, "topics":  [{{"topicName": String, "ifLab_title": String, "ifAssignment_title": String, "ifExam_title": String, "ifQuiz_title": String, readings: [{{"textBook": String, "chapter": Int}}]}}]}}]
    
        Output week {week} only.
    """
    response = create_chat_model_prompt(initial_prompt)

    # Parsing and cleaning up the content
    content_dict = parse_response_content(response)
    content_dict_no_newlines = remove_newlines(content_dict)

    return content_dict_no_newlines, 200


# After the teacher has gotten the entire weeklyContent they may want to update a specific week, that's what this endpoint is for
@app.route("/updateWeekContent", methods=["POST"])
def updateWeekContent():
    # get the entire json
    data = request.get_json()
    week = data.get("week")
    course_json = data.get("course")

    prompt = f"""
        Regenerate the outline for weeklyContent week {week} given this object:
        {course_json}
        
        Please output the weekly outline in json format defined as follows:
        
        weeklyContent: [{{"week": Int, "topics":  [{{"topicName": String, "ifLab_title": String, "ifAssignment_title": String, "ifExam_title": String, "ifQuiz_title": String, readings: [{{"textBook": String, "chapter": Int}}]}}]}}]
    """

    response = create_chat_model_prompt(prompt)

    # Parsing and cleaning up the content
    content_dict = parse_response_content(response)
    content_dict_no_newlines = remove_newlines(content_dict)

    return content_dict_no_newlines, 200


@app.route("/getClassOutline", methods=["POST"])
def getClassOutline():
    data = request.get_json()
    course = data.get("course")
    weekNumber = data.get("week")

    classesPerWeek = course.get("classesPerWeek")
    classLengthInHours = course.get("classLengthInHours")

    prePrompt = "Given this course: "
    prePrompt_plus_course = prePrompt + json.dumps(course, indent=4)
    conclusion = f"""Assuming I am a teacher, create a class outline
        for week {weekNumber} for a course with {classesPerWeek} classes per week, each lasting {classLengthInHours} hour.
        Include learning objectives, required materials, and a class procedure with time allocations.
        Output as JSON with this format: {{'week': Int, 'topics': [{{'topicName': String, 'readings': [String]}}],
        'classOutline': [{{'classNumber': Int, 'learningObjectives': [String], 'classProcedure': [{{'time': String,
        'activity': String}}], 'requiredMaterials': [String]}}]}}"""

    final_prompt = prePrompt_plus_course + "\n" + conclusion

    res = create_chat_model_prompt(final_prompt)
    content_dict = parse_response_content(res)
    content_dict_no_newlines = remove_newlines(content_dict)

    return content_dict_no_newlines, 200


# Input for layer 3 prompt:
# Input topics + the topicIndex
@app.route("/getNotesOutlineForTopic", methods=["POST"])
def getNotesOutlineForTopic():
    data = request.get_json()
    topics = data.get("topics")
    topicNumber = data.get("topicIndex")

    prePrompt = "Given these topics:"
    prePrompt_plus_topics = prePrompt + json.dumps(topics, indent=4)
    conclusion = f"""Create an outline of topic {topicNumber} with bullets on what will be discussed so we can use 
        this outline to make notes for the students. Output in json with this format:
        {{"topicName": String, "readings": [String], "outline": [{{"heading": String, "subtopics": [String]}}]}}
    """

    final = prePrompt_plus_topics + "\n" + conclusion

    res = create_chat_model_prompt(final)
    responseWithNewLine = res.choices[0].message["content"]
    content_dict = json.loads(responseWithNewLine)
    contentNoNewLines = remove_newlines(content_dict)

    return contentNoNewLines, 200


# layer 4 prompt
@app.route("/getOutlineForSubtopic", methods=["POST"])
def getOutlineForSubtopic():
    # returns = {"title": "Sub bitch x 4"}

    data = request.get_json()
    outlines = data.get("outline")
    outlineIndex = data.get("outlineIndex")
    subtopicIndex = data.get("subtopicIndex")

    prePrompt = "Given these outlines: "
    midPrompt = prePrompt + json.dumps(outlines, indent=4)
    conclusion = f"""Create an outline of what should be discussed within the 
        subtopic for the subsections of each outline[{outlineIndex}]["subtopic"][{subtopicIndex}]. Output in this JSON format:
        {{"subtopic": {{"title": String, "outline": [String]}}}}"""

    final = midPrompt + "\n" + conclusion

    res = create_chat_model_prompt(final)
    responseWithNewLine = res.choices[0].message["content"]
    content_dict = json.loads(responseWithNewLine)
    contentNoNewLines = remove_newlines(content_dict)

    return contentNoNewLines, 200


# layer 5 prompt
@app.route("/writeContentForSubtopic", methods=["POST"])
def writeContentForSubtopic():
    returns = {"title": "Sub bitch x 4"}

    return returns, 200


if __name__ == "__main__":
    app.run(debug=True, port=3000)
