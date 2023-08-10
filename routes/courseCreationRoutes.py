from flask import request, Blueprint
from helpers import create_chat_model_prompt, parse_response_content
import json

# Create a Blueprint instance
bp = Blueprint("courseCreation", __name__)


@bp.route("/courseCreation/generateCurriculum", methods=["POST"])
def generateCurriculum():
    userPrompt = request.get_json()
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
    content_dict = parse_response_content(response)

    return content_dict, 200


@bp.route("/courseCreation/generateSubTopicsForUnit", methods=["POST"])
def generateSubTopicsForUnit():
    data = request.get_json()
    curriculum = data.get("curriculum")
    unitNumber = data.get("unitNumber")
    prompt = f"""
        Given this curriculum:
        {curriculum},
        
        Create a list of subtopics for unit number {unitNumber}. Make sure to take the other units into consideration before making the subtopics.

        output in this json format:

        {{"subUnits": [{{"unitTitle": String, "unitDescription": String, "unitNumber": Double}}]}}
        
        Do not respond to this message, simply output the JSON object.
    """
    response = create_chat_model_prompt(prompt)
    content_dict = parse_response_content(response)

    return content_dict, 200


@bp.route("/courseCreation/generateLessonsForSubunit", methods=["POST"])
def generateLessonsForSubunit():
    data = request.get_json()
    curriculum = data.get("curriculum")
    subunitNumber = data.get("subunitNumber")
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
    print(response)
    content_dict = parse_response_content(response)

    return content_dict, 200


@bp.route("/courseCreation/generateNotesForLesson", methods=["POST"])
def generateNotesForLesson():
    data = request.get_json()
    unit = data.get("unit")
    lessonNumber = data.get("lessonNumber")

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
    print(response)
    content_dict = parse_response_content(response)

    return content_dict, 200


@bp.route("/courseCreation/getWeeklyContent", methods=["POST"])
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

        weeklyContent: {{"week": Int, "assessments": [{{"assessmentType": String, "assessmentTitle": String, "assessmentDescription": String}}], "topics":  [{{"topicName": String, readings: [{{"textbook": String, "chapter": Int}}]}}]}}
    
        Output week {week} only.
        
        Do not respond to this message, simply output the JSON.
    """
    response = create_chat_model_prompt(initial_prompt)

    # Parsing and cleaning up the content
    content_dict = parse_response_content(response)

    return content_dict, 200


# After the teacher has gotten the entire weeklyContent they may want to update a specific week, that's what this endpoint is for
@bp.route("/courseCreation/updateWeekContent", methods=["POST"])
def updateWeekContent():
    # get the entire json
    data = request.get_json()
    week = data.get("week")
    course_json = data.get("course")

    prompt = f"""
        Regenerate the outline for weeklyContent week {week} given this object:
        {course_json}
        
        Please output the weekly outline in json format defined as follows:
        
        weeklyContent: {{"week": Int, "assessments": [{{"assessmentType": String, "assessmentTitle": String, "assessmentDescription": String}}], "topics":  [{{"topicName": String, readings: [{{"textbook": String, "chapter": Int}}]}}]}}
        Do not respond to this message, simply output the JSON.
    """

    response = create_chat_model_prompt(prompt)

    # Parsing and cleaning up the content
    content_dict = parse_response_content(response)

    return content_dict, 200


@bp.route("/courseCreation/getClassOutline", methods=["POST"])
def getClassOutline():
    data = request.get_json()
    course = data.get("course")
    weekNumber = data.get("week")

    courseTimingStructure = course.get("courseTimingStructure")
    classesPerWeek = courseTimingStructure.get("classesPerWeek")
    classLengthInHours = courseTimingStructure.get("classLengthInHours")

    prePrompt = "Given this course: "
    prePrompt_plus_course = prePrompt + json.dumps(course, indent=4)
    conclusion = f"""
        Assuming I am a teacher, create a class outline for week {weekNumber} for a course with {classesPerWeek} classes per 
        week, each lasting {classLengthInHours} hour.
        
        Include learning objectives, required materials, and a class procedure with time allocations.
        
        Output as JSON with this format: 
        {{'classOutline': [{{'classNumber': Int, 'learningObjectives': [String], 'classProcedure': [{{'time': String, 'activity': String}}], 'requiredMaterials': [String]}}]}}
        
        Do not respond to this message, simply output the JSON.
        """

    final_prompt = prePrompt_plus_course + "\n" + conclusion

    res = create_chat_model_prompt(final_prompt)
    content_dict = parse_response_content(res)

    return content_dict, 200


@bp.route("/courseCreation/getNotesOutlineForTopic", methods=["POST"])
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
        
        {{"outline": [{{"heading": String, "subtopics": [String]}}]}}
        
        Do not respond to this message, simply output the JSON.
    """

    final = prePrompt_plus_topics + "\n" + conclusion

    res = create_chat_model_prompt(final)
    content_dict = parse_response_content(res)

    return content_dict, 200


@bp.route("/courseCreation/getOutlineForSubtopic", methods=["POST"])
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
        
        {{"title": String, "outline": [String]}}
        
        Do not respond to this message, simply output the JSON object.
        """

    final = midPrompt + "\n" + conclusion

    res = create_chat_model_prompt(final)
    content_dict = parse_response_content(res)

    return content_dict, 200


@bp.route("/courseCreation/getOutlineForSubSubtopic", methods=["POST"])
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

    return content_dict, 200


@bp.route("/courseCreation/writeContentForSubtopic", methods=["POST"])
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

    return content_dict, 200


@bp.route("/courseCreation/addDepth", methods=["POST"])
def addDepth():
    data = request.get_json()

    outline = data.get("outline")
    title = data.get("title")
    content = data.get("content")

    prompt = f"""
        Given this outline for the week:
        
        {outline},
        
        and the notes for this section:
        
        {title},
        {content},
        
        Add more depth to the notes by making it more comprehensive while making sure not to overlap with other subtopics in the outline.
        
        Output in this JSON format:
        
        {{"title": String, "content": String}}
        
        Do not respond to this message, simply output the JSON object.
    """

    response = create_chat_model_prompt(prompt)

    # Parsing and cleaning up the content
    content_dict = parse_response_content(response)

    return content_dict, 200
