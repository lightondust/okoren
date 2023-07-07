from datetime import datetime
import uuid
import os
import json


class Conversation:
    def __init__(self, initial_system_message=None, id=None, from_file=None):
        if from_file:
            with open(from_file, 'r') as infile:
                self.conversation = json.load(infile)
            self.id = os.path.splitext(os.path.basename(from_file))[0]
        else:
            self.id = str(uuid.uuid4()) if id is None else id
            self.conversation = [{"role": "system", "content": initial_system_message, "time": datetime.now().isoformat()}]

    def add_message(self, role, content, time=None):
        assert role in ["system", "user", "assistant"], "Invalid role, should be 'system', 'user', or 'assistant'"
        if time is None:
            time = datetime.now().isoformat()
        self.conversation.append({"role": role, "content": content, "time": time})

    def update_system_message(self, content, time=None):
        for message in self.conversation:
            if message['role'] == 'system':
                message['content'] = content
                if time is not None:
                    message['time'] = time
                break

    def get_conversation(self, for_db=False):
        if for_db:
            return self.conversation
        else:
            return [{"role": message["role"], "content": message["content"]}
                    for message in self.conversation]

    def save_conversation(self, directory="data/conversations"):
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(os.path.join(directory, f"{self.id}.json"), 'w') as outfile:
            json.dump(self.get_conversation(for_db=True), outfile)