from openai import OpenAI

class AIClient():
    def __init__(self, url, api_key, model):
        self.client = OpenAI(
            base_url = url,
            api_key=api_key, # required, but unused
        )
        self.model=model
        self.test_connection()

    def test_connection(self):
        return self.client.models.list()

    def chat(self, messages):
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return resp
    
    def chat_stream(self, messages):
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True
        )
        return stream
