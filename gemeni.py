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

#dont use
def generate(input):
    """client = genai.Client(api_key=os.getenv("GEMINI_KEY"))
    print("client")"""
    generativeai.configure(api_key=os.getenv("GEMINI_KEY"))
    model_name = "gemini-2.0-flash-001"
    model = generativeai.GenerativeModel(model_name=model_name)
    response = model.generate_content(input)
    return response.text
    """chat = client.chats.create(model = "gemini-2.0-flash")
    response = chat.send_message(input)
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
    )
    return response.text"""



print(generate("I have a headache"))
