import openai
import json
import re


def remove_control_characters(s):
    return re.sub(r"[\x00-\x1F\x7F]", "", s)


def create_chat_model_prompt(content: str, n=1) -> dict:
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        n=n,
        messages=[
            {"role": "user", "content": content},
        ],
    )


def parse_response_content(response):
    content = response.choices[0].message["content"]
    gucci = remove_control_characters(content)
    return json.loads(gucci)


def parse_multiple_response_content(response):
    all_messages = {}
    for i, choice in enumerate(response.choices):
        content = choice.message["content"]
        clean_content = remove_control_characters(content)
        all_messages[f"message_{i}"] = json.loads(clean_content)
    return all_messages
