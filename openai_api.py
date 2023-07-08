import openai


class OpenAI_API:
    def __init__(self, api_key, model):
        openai.api_key = api_key
        self.model = model

    def generate_reply(self, conversation):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=conversation.get_conversation()
        )
        token_count = response['usage']['total_tokens']
        return response.choices[0].message['content'], token_count
