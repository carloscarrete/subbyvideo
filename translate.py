import deepl
from dotenv import load_dotenv
import os

load_dotenv() 

# Authenticate with DeepL API 
auth_key = os.getenv('API_TRANSLATE')
translator = deepl.Translator(auth_key)

def translate_now(file):
    input_path = file
    output_path = file
    with open(input_path, 'r') as f:
        text = f.read()
    result = translator.translate_text(text, target_lang='ES')
    translated_text = result.text
    with open(output_path, 'w') as f:
        f.write(translated_text)
    print('Document translated to Spanish and saved to', output_path)