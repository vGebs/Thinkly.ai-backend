from dotenv import load_dotenv
import os
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": """ 
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

weeklyContent: [{"week": Int, "topics":  [{topicName: String, readings: [String]}]}]
         """,
        },
    ],
)

# print("Respone: --------------------->>>")
# print(response)

import json

# assuming 'response' is the OpenAI object
content = response.choices[0].message["content"]

# parse the content
content_dict = json.loads(content)


def remove_newlines(obj):
    if isinstance(obj, str):
        return obj.replace("\n", " ")  # replace newline with space
    elif isinstance(obj, list):
        return [remove_newlines(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: remove_newlines(value) for key, value in obj.items()}
    else:
        return obj


content_dict_no_newlines = remove_newlines(content_dict)

# Now content_dict_no_newlines is a Python dictionary with no newlines.
# print("")
# print("Content with no new lines: ---------------------->>>")
# print(content_dict_no_newlines)

# print("")
# print("Course Name:------------------------>>>")
# print(content_dict_no_newlines["courseName"])

# print("")
# print("WeeklyContent[0]:------------------------>>>")
# print(content_dict_no_newlines["weeklyContent"][0])

weeklyContent = content_dict_no_newlines["weeklyContent"]

prePrompt = "Given this course: "
prePrompt_plus_course = prePrompt + json.dumps(content_dict_no_newlines, indent=4)

for index, week in enumerate(weeklyContent):
    weekNumber = week["week"]
    classesPerWeek = content_dict_no_newlines["classesPerWeek"]
    classLengthInHours = content_dict_no_newlines["classLengthInHours"]

    conclusion = f"""Assuming I am a teacher, create a class outline
        for week {weekNumber} for a course with {classesPerWeek} classes per week, each lasting {classLengthInHours} hour.
        Include learning objectives, required materials, and a class procedure with time allocations.
        Output as JSON with this format: {{'week': Int, 'topics': [{{'topicName': String, 'readings': [String]}}],
        'classOutline': [{{'classNumber': Int, 'learningObjectives': [String], 'classProcedure': [{{'time': String,
        'activity': String}}], 'requiredMaterials': [String]}}]}}"""

    final = prePrompt_plus_course + "\n" + conclusion

    # print(final)

    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": final}]
    )

    # update the current week content with the response from the API
    responseWithNewLine = res.choices[0].message["content"]

    content_dict = json.loads(responseWithNewLine)

    contentNoNewLines = remove_newlines(content_dict)
    weeklyContent[index] = contentNoNewLines


finalObject = content_dict_no_newlines

finalObject["weeklyContent"] = weeklyContent

print("Final object: ------------------------->")
print(finalObject)
