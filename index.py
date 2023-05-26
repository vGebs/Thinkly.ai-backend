from dotenv import load_dotenv
import os
import openai
import json

# Set up OpenAI API
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def create_chat_model_prompt(content: str) -> dict:
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": content},
        ],
    )


def remove_newlines(obj):
    if isinstance(obj, str):
        return obj.replace("\n", " ")
    elif isinstance(obj, list):
        return [remove_newlines(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: remove_newlines(value) for key, value in obj.items()}
    else:
        return obj


def parse_response_content(response):
    content = response.choices[0].message["content"]
    return json.loads(content)


def create_final_prompt(content_dict_no_newlines, week, index):
    weekNumber = week["week"]
    classesPerWeek = content_dict_no_newlines["classesPerWeek"]
    classLengthInHours = content_dict_no_newlines["classLengthInHours"]

    prePrompt = "Given this course: "
    prePrompt_plus_course = prePrompt + json.dumps(content_dict_no_newlines, indent=4)
    conclusion = f"""Assuming I am a teacher, create a class outline
        for week {weekNumber} for a course with {classesPerWeek} classes per week, each lasting {classLengthInHours} hour.
        Include learning objectives, required materials, and a class procedure with time allocations.
        Output as JSON with this format: {{'week': Int, 'topics': [{{'topicName': String, 'readings': [String]}}],
        'classOutline': [{{'classNumber': Int, 'learningObjectives': [String], 'classProcedure': [{{'time': String,
        'activity': String}}], 'requiredMaterials': [String]}}]}}"""

    return prePrompt_plus_course + "\n" + conclusion


def create_final_object(content_dict_no_newlines, weeklyContent):
    finalObject = content_dict_no_newlines
    finalObject["weeklyContent"] = weeklyContent
    return finalObject


# Initial OpenAI request
initial_prompt = """ 
    Generate a course outline based on the following details:
    {
        "courseName": "Introduction to Philosophy",
        "courseDurationInWeeks": 15,
        "classLengthInHours": 1,
        "classesPerWeek": 3,
        "studyHoursPerWeek": 10,
        "gradeLevel": "University - Year 1",
        "textBookReferences": ["Problems of Philosophy by Bertrand Russell", "Meditations on First Philosophy by René Descartes"],
        "learningObjectives": ["Introduce students to key philosophical ideas", "Develop critical thinking skills"],
        "preRequisites": ["Basic understanding of logical reasoning"],
        "topicPreferences": ["Ethics", "Epistemology", "Metaphysics"]
    }
    Please output the course outline in json with all input fields plus an output field defined as follows: 
    Only output the first week.
    weeklyContent: [{"week": Int, "topics":  [{"topicName": String, readings: [String]}]}]
"""
response = create_chat_model_prompt(initial_prompt)

# Parsing and cleaning up the content
content_dict = parse_response_content(response)
content_dict_no_newlines = remove_newlines(content_dict)
weeklyContent = content_dict_no_newlines["weeklyContent"]

# Iterating over weeks for new requests and updates
for index, week in enumerate(weeklyContent):
    final_prompt = create_final_prompt(content_dict_no_newlines, week, index)
    res = create_chat_model_prompt(final_prompt)
    responseWithNewLine = res.choices[0].message["content"]
    content_dict = json.loads(responseWithNewLine)
    contentNoNewLines = remove_newlines(content_dict)
    weeklyContent[index] = contentNoNewLines

# Creating final object and print
finalObject = create_final_object(content_dict_no_newlines, weeklyContent)
# print("Final object: ------------------------->")
# print(finalObject)

# Everything is correct down to here

# ok, we have the final object.
# now we need to loop through the class outline for each day of each week and make an outline for the notes

weeklyContent = finalObject["weeklyContent"]

for index, week in enumerate(weeklyContent):
    topics = week["topics"]
    for index2, topic in enumerate(topics):
        prePrompt = "Given these topics"
        prePrompt_plus_topics = prePrompt + json.dumps(topics, indent=4)
        topicNumber = index2 + 1
        conclusion = f"""Create an outline of topic {topicNumber} with bullets on what will be discussed so we can use 
            this outline to make notes for the students. Output in json with this format:
            {{'topicName': 'String', 'readings': ['String'], 'outline': [{{'heading': 'String', 'subtopics': ['String']}}]}}
        """

        final = prePrompt_plus_topics + "\n" + conclusion

        res = create_chat_model_prompt(final)
        responseWithNewLine = res.choices[0].message["content"]
        content_dict = json.loads(responseWithNewLine)
        contentNoNewLines = remove_newlines(content_dict)
        weeklyContent[index]["topics"][index2] = contentNoNewLines


newFinalObject = create_final_object(finalObject, weeklyContent)
print("Final object: ------------------------->")
print(newFinalObject)
