import openai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('OPENAI_API')
model_id= 'whisper-1'
def get_subtitles(file):
    media__file = open(file, 'rb')
    response = openai.Audio.transcribe(
        model=model_id,
        file=media__file,
        api_key=API_KEY,
        response_format='srt'
    )
    with open(file.replace('.mp3','.srt'), 'w') as f:
        f.write(response)
    print('finished')

def translate_sub(file):
    media__file = open(file, 'rb')
    response = openai.Audio.translate(
        model=model_id,
        file=media__file,
        api_key=API_KEY,
        response_format='srt'
    )
    with open(file.replace('.mp3','.srt'), 'w') as f:
        f.write(response)
    print('finished')