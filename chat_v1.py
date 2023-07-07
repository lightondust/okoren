from openai_api import OpenAI_API
from conversation import Conversation
from system_message import system_message
from auth import get_auth


def initialize_conversation(api_key, model, system_message):
    api = OpenAI_API(api_key, model)
    conversation = Conversation(system_message)
    return api, conversation


def handle_user_input(api, conversation, user_message):
    conversation.add_message("user", user_message)
    ai_reply = api.generate_reply(conversation)
    conversation.add_message("assistant", ai_reply)
    print(ai_reply)


# Usage:
api, conversation = initialize_conversation(get_auth()['token'], 'gpt-3.5-turbo', system_message)

while True:
    # When a user message comes in
    user_message = input("Your message: ")
    handle_user_input(api, conversation, user_message)