from openai import OpenAI

class AIClient():
    def __init__(self, url, api_key, model):
        self.client = OpenAI(
            base_url = url,
            api_key=api_key, # required, but unused
        )
        self.model=model


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
