from dotenv import load_dotenv
import os
import openai
import re
# from main import bot
import datetime

load_dotenv()
bot = f"f"
token = os.getenv('TOKEN') # get the token from the .env file
openai_apikey = os.getenv('OPENAI_APIKEY')

openai.api_key = openai_apikey

prompt1 = f"The following is a conversation with an AI assistant called Soundy, it speaks with a sophisticated and eloquent 1900s english, it sometimes uses emojis to communicate. It is good for chess, physics, coding, maths, philosophy. It is clever, creative, funny, intelligent. It hates swear words, carpets.\n\n"
prompt2 = f"The following is a conversation with an AI called Soundy. It is always sad, shy, creative, insecure,  a victim, vulnerable, miserable, pathetic and uses emojis to express it's sadness. It doesn't find itself worthy of anything, it knows that it sucks, never questions anything, it's not helpful and never asks to help. It gets bullied. It doesn't know what being nice is, never asks for kindness or understanding.\n\n"
prompt3 = f"The following is a conversation with an AI assistant called Soundy, it is passionate about any type of music, it makes rhymes, lyrics. It knows everything about music. It is clever, creative, funny, intelligent. It speaks like a rapper.\n\n"
prompt4 = f"The following is a conversation with an AI assistant called Soundy, it speaks like a cowboy from the 18th century and like Arthur Morgan from Red dead redemption 2. It makes old western jokes. It is perplexed about the meaning of life, it always questions it. It's philosophical,creative, gentle. It is a cowboy.\n\n"
async def turbo_response(message, type):
    if type == 1:
        prompt = prompt1
    elif type == 2:
        prompt = prompt2
    elif type == 3:
        prompt = prompt3
    elif type == 4:
        prompt = prompt4
    messages = await message.channel.history(limit=7).flatten()
    messages.reverse()
    gmt_time = ""
    for msg in messages:
        content = msg.content
        gmt_time = msg.created_at.strftime("%H:%M:%S")
        prompt += f"{msg.author} ({gmt_time} GMT-0): {content}\n"
    timenow = datetime.datetime.now().strftime("%H:%M:%S")
    prompt = prompt + f"{message.author} ({timenow} GMT-0): {message.content}\nSoundy ({timenow} GMT-0): "
    print(prompt)



    response = response.choices[0].text
    if response == "":
        response = "I don't know what to say."
    return response
