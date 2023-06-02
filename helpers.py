import openai
import json
import re


def remove_control_characters(s):
    return re.sub(r"[\x00-\x1F\x7F]", "", s)


def create_chat_model_prompt(content: str) -> dict:
    return openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": content},
        ],
    )


def parse_response_content(response):
    content = response.choices[0].message["content"]
    gucci = remove_control_characters(content)
    return json.loads(gucci)
