import os.path

from openai_api import OpenAI_API
from conversation import Conversation
from system_message import system_message
from auth import get_auth


def initialize_conversation(api_key, model, system_message, from_file=None):
    api = OpenAI_API(api_key, model)
    conversation = Conversation(system_message, from_file=from_file)

    if from_file:
        messages = conversation.get_conversation()
        for m in messages:
            print_message(m['content'], m['role'])

    return api, conversation


def handle_user_input(api, conversation, user_message):
    conversation.add_message("user", user_message)
    ai_reply = api.generate_reply(conversation)
    conversation.add_message("assistant", ai_reply)
    print_message(ai_reply, 'assistant')
    conversation.save_conversation(directory=save_to)


def print_message(message, role):
    if role == 'assistant':
        print()
        print('-------------------------')
        print(message)
    elif role == 'user':
        print()
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print('your message: ')
        print(message)


if __name__ == '__main__':
    save_to = 'data/conversations'

    conversation_id = input('Conversation id:')
    from_file = '{}/{}.json'.format(save_to, conversation_id)
    if not os.path.exists(from_file):
        from_file = None
        conversation_id = None

    api, conversation = initialize_conversation(get_auth()['token'], 'gpt-3.5-turbo', system_message, from_file=from_file)

    print('conversation start({}):'.format(conversation.id))

    while True:

        # When a user message comes in
        print_message('', 'user')
        user_message = input()
        handle_user_input(api, conversation, user_message)