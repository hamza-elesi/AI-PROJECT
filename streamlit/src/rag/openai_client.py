import openai
import os

class OpenAIClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def generate_response(self, prompt: str) -> str:
        """
        Generate a response from OpenAI's GPT API.
        :param prompt: The prompt to send to GPT.
        :return: Generated response.
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an SEO assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )
            return response.choices[0].message["content"]
        except Exception as e:
            return f"Error generating response: {str(e)}"
