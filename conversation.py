class Conversation:
    def __init__(self, initial_system_message):
        self.conversation = [{"role": "system", "content": initial_system_message}]

    def add_message(self, role, content):
        assert role in ["system", "user", "assistant"], "Invalid role, should be 'system', 'user', or 'assistant'"
        self.conversation.append({"role": role, "content": content})

    def update_system_message(self, content):
        for message in self.conversation:
            if message['role'] == 'system':
                message['content'] = content
                break

    def get_conversation(self):
        return self.conversation
