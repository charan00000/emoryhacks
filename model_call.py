from transformers import AutoModelForCausalLM, AutoTokenizer
import  kagglehub
import os

from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi()
api.authenticate()

VERSION_NUMBER = "v1"

VARIATION_SLUG = "medgenius_llama-3.2b"

FRAMEWORK = "transformers"

# Download latest version
os.makedirs('kaggle/input', exist_ok=True)
path = kagglehub.model_download("huzefanalkheda/medgenius_llama-3.2bv1/transformers/medgenios")

print("Path to model files:", path)
PATH = f"/kaggle/input/huzefanalkheda/transformers/medgenios/1"

MODEL_NAME = f"/kaggle/input/medgenius_llama-3.2bv1/transformers/medgenios/1/model"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

input_text = "What are the symptoms of diabetes?"

input_ids = tokenizer.encode(input_text, return_tensors='pt')

output = model.generate(input_ids)

response = tokenizer.decode(output[0], skip_special_tokens=True)

print(response)
