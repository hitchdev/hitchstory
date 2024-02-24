from openai import OpenAI
from pathlib import Path
import json

OPENAI_API_KEY = Path(__file__).parents[0].joinpath("OPENAI_API_KEY").read_text().rstrip()


class LLMAnswers:
    def __init__(self):
        self._client = OpenAI(api_key=OPENAI_API_KEY)
        self._prompt = "You should answer questions about the following text:\n\n{context}"

    def ask(self, context, question):
        response = self._client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self._prompt.format(context=context)},
                {"role": "user", "content": question},
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return json.loads(response.json())["choices"][0]["message"]["content"]


class LLMClient:
    def __init__(self, prompt):
        self._client = OpenAI(api_key=OPENAI_API_KEY)
        self._prompt = prompt
        
    def run(self):
        response = self._client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": self._prompt}],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return json.loads(response.json())["choices"][0]["message"]["content"]


class LLMServer:
    def __init__(self, prompt):
        self._client = OpenAI(api_key=OPENAI_API_KEY)
        self._prompt = prompt
        
    def run(self, messages):
        response = self._client.chat.completions.create(
            response_format={"type": "json_object"},
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "system", "content": self._prompt}] + messages,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return json.loads(response.json())["choices"][0]["message"]["content"]
