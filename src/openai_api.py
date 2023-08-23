import openai
import os
from dotenv import load_dotenv

# token should be either stored in .env or as github token
if os.getenv("GITHUB_ACTIONS"):
    openai_token = os.getenv("OPENAI_TOKEN")
else:
    load_dotenv()
    openai_token = os.getenv("OPENAI_TOKEN")

openai.api_key = openai_token

def get_gpt_response(messages):
    try: 
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        feedback = response['choices'][0]['message']['content'].replace('"', '')
        return feedback
    except:
        feedback = "We are too busy, try to ask later..."
        return feedback