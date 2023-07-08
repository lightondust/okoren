from datetime import datetime
import uuid
import os
import json
import tiktoken


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def transform_message(message):
    keys = ['role', 'content']
    return {k:message.get(k) for k in keys}


class Conversation:
    def __init__(self, initial_system_message=None, id=None, from_file=None):
        if from_file:
            with open(from_file, 'r') as infile:
                self.conversation = json.load(infile)
            self.id = os.path.splitext(os.path.basename(from_file))[0]
        else:
            self.id = str(uuid.uuid4()) if id is None else id
            self.conversation = [{"role": "system", "content": initial_system_message, "time": datetime.now().isoformat()}]

    def add_message(self, role, content, token_count=None, time=None):
        assert role in ["system", "user", "assistant"], "Invalid role, should be 'system', 'user', or 'assistant'"
        if time is None:
            time = datetime.now().isoformat()
        self.conversation.append({"role": role, "content": content, "time": time, "token_count": token_count})
        print('message_token_count: {}'.format(self.count_total_token()))

    def count_total_token(self):
        return num_tokens_from_messages([transform_message(m) for m in self.conversation])

    def update_system_message(self, content, time=None):
        for message in self.conversation:
            if message['role'] == 'system':
                message['content'] = content
                if time is not None:
                    message['time'] = time
                break

    def get_conversation(self, for_db=False, max_tokens=4096-500):
        if for_db:
            return self.conversation
        else:
            total_tokens = 0
            system_message = transform_message(self.conversation[0])
            total_tokens += num_tokens_from_messages([system_message])

            truncated_conversation = []
            for message in reversed(self.conversation[1:]):
                message = transform_message(message)
                total_tokens += num_tokens_from_messages([message])
                if total_tokens > max_tokens:
                    break
                truncated_conversation.append(message)

            # Prepend system message to the conversation
            truncated_conversation.append(system_message)
            return list(reversed(truncated_conversation))

    def save_conversation(self, directory="data/conversations"):
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(os.path.join(directory, f"{self.id}.json"), 'w') as outfile:
            json.dump(self.get_conversation(for_db=True), outfile, ensure_ascii=False, indent=4)
