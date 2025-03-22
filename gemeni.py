from google import genai
from google.genai import types
import os
import base64
from dotenv import load_dotenv

load_dotenv('keys/.env')

def conversation():
    client = genai.Client(api_key=os.getenv('GEMENI_KEY'))
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


def generate(input):
    client = genai.Client(api_key=os.getenv("GEMINI_KEY"))
    response = client.models.generate_content(
        model = "gemini-2.0-flash",
        contents = input,
    )
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
    )

    print(response.text)

if __name__ == "__main__":
    conversation()
    generate("I have a headache")
