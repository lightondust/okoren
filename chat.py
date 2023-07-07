import openai

from auth import get_auth
from system_message import system_message

# openai.api_key = 'your_openai_secret_key'
openai.api_key = get_auth()['token']

# 霊子の性格と説明

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