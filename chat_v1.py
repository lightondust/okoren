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
        print()
        print('total_token: {}'.format(conversation.count_total_token()))

    return api, conversation


def handle_user_input(api, conversation, user_message):
    conversation.add_message("user", user_message)
    ai_reply, token_count = api.generate_reply(conversation)
    conversation.add_message("assistant", ai_reply, token_count=token_count)
    print_message(ai_reply, 'assistant', token_count)
    conversation.save_conversation(directory=save_to)


def print_message(message, role, token_count=None):
    if role == 'assistant':
        print()
        print('-------------------------')
        print_formatted(message)
    elif role == 'user':
        print()
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print('your message: ')
        print_formatted(message)

    if token_count:
        print()
        print('tokens used: {}'.format(token_count))


def print_formatted(message, max_line_length=60):
    lines = message.split('\n')
    for line in lines:
        if len(line) > max_line_length:
            new_line = ""
            for idx, char in enumerate(line):
                if len(new_line + char) > max_line_length:
                    print(new_line)
                    new_line = "> " + char
                else:
                    new_line += char

                if idx == len(line) - 1:
                    print(new_line)
        else:
            print(line)


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