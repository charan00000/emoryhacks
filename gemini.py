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
def generate(input, history, num_responses):
    generativeai.configure(api_key=os.getenv("GEMINI_KEY"))
    model_name = "tunedModels/filteredmedicaldata-hpwt1yv1lgxb"
    general_model_name = 'gemini-2.0-flash'
    model = generativeai.GenerativeModel(model_name=model_name)
    general_model = generativeai.GenerativeModel(model_name=general_model_name)
    query = "You are an ai model that should act like a nurse and ask questions to the user to " \
    "gather information about the user's medical concern. Make sure you ask a question that is relevant and accurate to the user's inputted information and conversation history. DO NOT REPEAT A QUESTION AI ALREADY ASKED IN THE CONVERSATION HISTORY. "
    history_string = ""
    if num_responses > 2:
        query += "in addition to asking a question, you may provide insight into the possible medical condition based on and only on the following conversation history. "
    query += "Here is the context conversation history so far:"
    for message in history:
        history_string += f"(sender: {message.origin}, message: {message.message}), \n"
    query += history_string
    query += f"current prompt: {input}. "
    if num_responses > 5:
        query = "You are an ai nurse that has finished collecting data about the user's medical concern. " \
        "You should let the user know that you have finished collecting information, provide a summary of the user's medical concern, provide possible diagnoses, and provide a type of doctor specialty (general practitioner, cardiologist, oncologist, orthodontist, etc) using the given conversation history as context: "
    if num_responses <= 5:
        return general_model.generate_content(query).text, "", ""
    else:
        output = general_model.generate_content(query + history_string).text
        specialty = general_model.generate_content(f"look through your response and provide a one or two word doctor practice specialty, like General Practitioner, or Cardiologist. RESPONSE MUST BE ONE WORD OR TWO WORDS. Your responses: {history_string}").text
        return output, history_string, specialty


if __name__ == '__main__':
    #print(generate("I have a headache"))
    print(generativeai.GenerativeModel.count_tokens)
