import openai
import json


def create_chat_model_prompt(content: str) -> dict:
    return openai.ChatCompletion.create(
        model="gpt-4",
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
