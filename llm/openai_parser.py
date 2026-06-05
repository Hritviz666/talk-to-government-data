import json
from openai import OpenAI

from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def load_system_prompt():

    with open(
        "prompts/parser_prompt.txt",
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()
    

def parse_question(question):

    system_prompt = load_system_prompt()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    content = response.choices[0].message.content

    return json.loads(content)