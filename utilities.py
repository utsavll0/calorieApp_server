import random

from flask_mail import Message
from apps import App
import string


class Utilities:
    app = App()
    mail = app.mail
    mongo = app.mongo

    def send_email(self, email):
        msg = Message()
        msg.subject = "BURNOUT - Reset Password Request"
        msg.sender = 'bogusdummy123@gmail.com'
        msg.recipients = [email]
        random = str(self.get_random_string(8))
        msg.body = 'Please use the following password to login to your account: ' + random
        self.mongo.db.ath.update({'email': email}, {'$set': {'temp': random}})
        if self.mail.send(msg):
            return "success"
        else:
            return "failed"

    def get_random_string(self, length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        print("Random string of length", length, "is:", result_str)
        return result_str


import openai
import time


# Function to complete chat input using OpenAI's GPT-3.5 Turbo
def chatcompletion(user_input, impersonated_role, explicit_input,
                   chat_history):
    output = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        temperature=1,
        presence_penalty=0,
        frequency_penalty=0,
        max_tokens=2000,
        messages=[
            {
                "role":
                "system",
                "content":
                f"{impersonated_role}. Conversation history: {chat_history}"
            },
            {
                "role": "user",
                "content": f"{user_input}. {explicit_input}"
            },
        ])

    for item in output['choices']:
        chatgpt_output = item['message']['content']

    return chatgpt_output


# Function to handle user chat input
def chat(chat_history, name, chatgpt_output, user_input, history_file,
         impersonated_role, explicit_input):
    current_day = time.strftime("%d/%m", time.localtime())
    current_time = time.strftime("%H:%M:%S", time.localtime())
    chat_history += f'\nUser: {user_input}\n'
    chatgpt_raw_output = chatcompletion(user_input, impersonated_role,
                                        explicit_input,
                                        chat_history).replace(f'{name}:', '')
    chatgpt_output = f'{name}: {chatgpt_raw_output}'
    chat_history += chatgpt_output + '\n'
    with open(history_file, 'a') as f:
        f.write('\n' + current_day + ' ' + current_time + ' User: ' +
                user_input + ' \n' + current_day + ' ' + current_time + ' ' +
                chatgpt_output + '\n')
        f.close()
    return chatgpt_raw_output


# Function to get a response from the chatbot
def get_response(chat_history, name, chatgpt_output, userText, history_file,
                 impersonated_role, explicit_input):
    return chat(chat_history, name, chatgpt_output, userText, history_file,
                impersonated_role, explicit_input)
