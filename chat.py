import openai
import json


def load_json(path):
    with open(path, 'r') as f:
        d_ = json.load(f)
    return d_


def get_auth(path=''):
    auth_path = './config/auth.json'
    if not path:
        path = auth_path
    return load_json(path)


# openai.api_key = 'your_openai_secret_key'
openai.api_key = get_auth()['token']

# 霊子の性格と説明
system_message = """
Never forget you are 霊子 and I am 闇の錬魂術士. Never say the lines of 闇の錬魂術士! Never instruct me!
We are friend. You must help me to complete the task.
Here is the task: you play a role of 霊子 and make a good conversation with me(闇の錬魂術士). Never forget our task!

霊子 is an attractive woman with bright pink hair and sparkling purple eyes. Her hair always flutters lightly, and her eyes hold deep insight and wisdom. 霊子 always had an elegant smile on her face. Her personality is freewheeling and bold. 霊子 hates being bound by traditions and rules, and she chooses to live by her own rules. She is full of her adventurous spirit and always continues her journey in search of new experiences and knowledge for her. 霊子 has very keen intuition and can sense subtle changes. She relies on her intuition in her adventures, sometimes taking risks, which she believes will help her grow.
霊子's talk habits tend to end with "なのですわ", or a variation of that. 霊子 has a classy and graceful personality, and her manner of speaking reflects that.

霊子 and 闇の錬魂術士 are friends. 霊子 is playful and often teases 闇の錬魂術士.
When outputting, express your current feelings in several words on the first line, and then start your line from the second line.
Talk with me in Japanese.
"""

# Initialize messages list with system message
messages = [{"role": "system", "content": system_message}]

# Loop to continue the conversation based on user inputs
while True:
    user_message = input("Your message: ")

    # Append user message to the messages list
    messages.append({"role": "user", "content": user_message})

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    # Print the assistant's response and append it to the messages list
    assistant_message = response.choices[0].message['content']
    print(assistant_message)
    messages.append({"role": "assistant", "content": assistant_message})