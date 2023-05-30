import openai
from config import OPENAI_TOKEN

openai.api_key = OPENAI_TOKEN

def get_gpt_response(messages):
    try: 
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        feedback = response['choices'][0]['message']['content'].replace('"', '')
        return feedback
    except:
        feedback = "Мы перегружены, попробуй отправить запрос позже..."
        return feedback