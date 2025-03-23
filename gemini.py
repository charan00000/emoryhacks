from google import genai
import google.generativeai as generativeai
from google.genai import types
import os
import base64
from dotenv import load_dotenv

load_dotenv('keys/.env')

#dont use
def conversation():
    client = genai.Client(api_key=os.getenv('GEMINI_KEY'))
    chat = client.chats.create(model="gemini-2.0-flash")

    response = chat.send_message_stream("I have 2 dogs in my house.")
    for chunk in response:
        print(chunk.text, end="")

    response = chat.send_message_stream("How many paws are in my house?")
    for chunk in response:
        print(chunk.text, end="")

    for message in chat.get_history():
        print(f'role - {message.role}', end=": ")
        print(message.parts[0].text)

#
def generate(input, history):
    generativeai.configure(api_key=os.getenv("GEMINI_KEY"))
    model_name = "tunedModels/filteredmedicaldata-hpwt1yv1lgxb"
    model = generativeai.GenerativeModel(model_name=model_name)
    query = "past question-answers in conversation: "
    for message in history:
        query += f"(sender: {message.origin}, message: {message.message}), "
    query += f"current question: {input}. If you believe that you have enough information to pass along to the doctor, you may tell the user that. If and only if the user does not provide a medical-related prompt, you can provide a general, non-medical related answer."
    response = model.generate_content(query)
    return response.text


if __name__ == '__main__':
    print(generate("I have a headache"))
