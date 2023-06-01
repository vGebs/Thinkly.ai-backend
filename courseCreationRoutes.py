from flask import request, Blueprint
from helpers import create_chat_model_prompt, parse_response_content, remove_newlines
import json

# Create a Blueprint instance
bp = Blueprint("courseCreation", __name__)


@bp.route("/getWeeklyContent", methods=["POST"])
def getWeeklyContent():
    # Get the entire JSON object
    data = request.get_json()
    week = data.get("week")
    course_json = data.get("course")

    # Initial OpenAI request
    initial_prompt = f""" 
        Generate a course outline based on the following details:
        {course_json}
        
        Please output the course outline in json defined as follows: 

        weeklyContent: {{"week": Int, "topics":  [{{"topicName": String, readings: [{{"textBook": String, "chapter": Int}}]}}]}}
    
        Output week {week} only.
        
        Do not respond to this message, simply output the JSON.
    """
    response = create_chat_model_prompt(initial_prompt)

    # Parsing and cleaning up the content
    content_dict = parse_response_content(response)
    content_dict_no_newlines = remove_newlines(content_dict)

    return content_dict_no_newlines, 200


# After the teacher has gotten the entire weeklyContent they may want to update a specific week, that's what this endpoint is for
@bp.route("/updateWeekContent", methods=["POST"])
def updateWeekContent():
    # get the entire json
    data = request.get_json()
    week = data.get("week")
    course_json = data.get("course")

    prompt = f"""
        Regenerate the outline for weeklyContent week {week} given this object:
        {course_json}
        
        Please output the weekly outline in json format defined as follows:
        
        weeklyContent: {{"week": Int, "topics":  [{{"topicName": String, readings: [{{"textBook": String, "chapter": Int}}]}}]}}
        Do not respond to this message, simply output the JSON.
    """

    response = create_chat_model_prompt(prompt)

    # Parsing and cleaning up the content
    content_dict = parse_response_content(response)
    content_dict_no_newlines = remove_newlines(content_dict)

    return content_dict_no_newlines, 200


@bp.route("/getClassOutline", methods=["POST"])
def getClassOutline():
    data = request.get_json()
    course = data.get("course")
    weekNumber = data.get("week")

    classesPerWeek = course.get("classesPerWeek")
    classLengthInHours = course.get("classLengthInHours")

    prePrompt = "Given this course: "
    prePrompt_plus_course = prePrompt + json.dumps(course, indent=4)
    conclusion = f"""
        Assuming I am a teacher, create a class outline for week {weekNumber} for a course with {classesPerWeek} classes per 
        week, each lasting {classLengthInHours} hour.
        
        Include learning objectives, required materials, and a class procedure with time allocations.
        
        Output as JSON with this format: 
        {{'week': Int, 'topics': [{{'topicName': String, 'readings': [String]}}], 'classOutline': [{{'classNumber': Int, 'learningObjectives': [String], 'classProcedure': [{{'time': String, 'activity': String}}], 'requiredMaterials': [String]}}]}}
        
        Do not respond to this message, simply output the JSON.
        """

    final_prompt = prePrompt_plus_course + "\n" + conclusion

    res = create_chat_model_prompt(final_prompt)
    content_dict = parse_response_content(res)
    content_dict_no_newlines = remove_newlines(content_dict)

    return content_dict_no_newlines, 200


@bp.route("/getNotesOutlineForTopic", methods=["POST"])
def getNotesOutlineForTopic():
    data = request.get_json()
    topics = data.get("topics")
    topicNumber = data.get("topicNumber")

    prePrompt = "Given these topics:"
    prePrompt_plus_topics = prePrompt + json.dumps(topics, indent=4)
    conclusion = f"""
        Create an outline for topic number {topicNumber} with bullets on what will be discussed so we can use 
        this outline to make notes for the students. 
        
        Output in json with this format:
        
        {{"topicName": String, "readings": [{{"textBook": String, "chapter": Int}}], "outline": [{{"heading": String, "subtopics": [String]}}]}}
        
        Do not respond to this message, simply output the JSON.
    """

    final = prePrompt_plus_topics + "\n" + conclusion

    res = create_chat_model_prompt(final)
    content_dict = parse_response_content(res)
    content_dict_no_newlines = remove_newlines(content_dict)

    return content_dict_no_newlines, 200


@bp.route("/getOutlineForSubtopic", methods=["POST"])
def getOutlineForSubtopic():
    data = request.get_json()

    outlineIndex = data.get("outlineIndex")
    subtopicIndex = data.get("subtopicIndex")
    outlines = data.get("outline")

    prePrompt = "Given these outlines: "
    midPrompt = prePrompt + json.dumps(outlines, indent=4)

    conclusion = f"""
        Create an outline for outline[{outlineIndex}]["subtopic"][{subtopicIndex}] with bullets on what will be discussed 
        so we can use this outline to make notes for the students. 
        
        Output in this JSON format:
        
        {{"subtopic": {{"title": String, "outline": [String]}}}}
        
        Do not respond to this message, simply output the JSON object.
        """

    final = midPrompt + "\n" + conclusion

    res = create_chat_model_prompt(final)
    content_dict = parse_response_content(res)
    content_dict_no_newlines = remove_newlines(content_dict)

    return content_dict_no_newlines, 200


@bp.route("/getOutlineForSubSubtopic", methods=["POST"])
def getOutlineForSubSubtopic():
    data = request.get_json()

    outlineNumber = data.get("outlineNumber")
    subtopic = data.get("subtopic")

    prePrompt = "Given this subtopic: "
    midPrompt = prePrompt + json.dumps(subtopic, indent=4)

    conclusion = f"""
    Create an outline for outline number {outlineNumber} with bullets on what will be discussed so we can use this outline to make 
    notes for students. 
    
    Ouput in this JSON format:
    
    {{"subtopic": {{"title": String, "outline": [String]}}}}

    Do not respond to this message, simply output the JSON object.
    """

    final = midPrompt + "\n" + conclusion

    res = create_chat_model_prompt(final)
    content_dict = parse_response_content(res)
    content_dict_no_newlines = remove_newlines(content_dict)

    return content_dict_no_newlines, 200


@bp.route("/writeContentForSubtopic", methods=["POST"])
def writeContentForSubtopic():
    data = request.get_json()

    outlineIndex = data.get("outlineIndex")
    subtopicIndex = data.get("subtopicIndex")
    subtopicOutlineIndex = data.get("subtopicOutlineIndex")

    outline = data.get("outline")

    prePrompt = "Given this outline: "
    midPrompt = prePrompt + json.dumps(outline, indent=4)

    conclusion = f"""
        Write a comprehensive piece for outline[{outlineIndex}]["subtopics"][{subtopicIndex}]["outline"][{subtopicOutlineIndex}] that 
        is approximately 3 paragraphs in length additionally, feel free to list some main concepts in bullet format.
    
        Output in this JSON format:
        {{"title": String, content: String}}
        
        Do not respond to this prompt, simply output the json.
    """

    final = midPrompt + "\n" + conclusion

    res = create_chat_model_prompt(final)
    content_dict = parse_response_content(res)
    content_dict_no_newlines = remove_newlines(content_dict)

    return content_dict_no_newlines, 200
