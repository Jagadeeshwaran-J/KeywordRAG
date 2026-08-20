from openai import OpenAI


class LLMClient:
    def __init__(self, base_url, model, api_key="EMPTY"):
        self.model = model
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )

    def generate(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a document question-answering assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        return response.choices[0].message.content