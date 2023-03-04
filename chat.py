from dotenv import load_dotenv
import os
import openai
import datetime
from config import c, bot, debug   
import re



load_dotenv()
token = os.getenv('TOKEN') # get the token from the .env file

async def response(message, type):
    model = ""
    try: 
        c.execute("SELECT * FROM model WHERE guild_id = ?", (message.guild.id,))
        model = c.fetchone()[1]
        print(model)
    except: model = "davinci"
    if type == 1:
        with open(f"./prompts/{model}/wise.txt", "r") as f:
            prompt = f.read()
    elif type == 2:
        with open(f"./prompts/{model}/bully.txt", "r") as f:
            prompt = f.read()
    elif type == 3:
        with open(f"./prompts/{model}/musical.txt", "r") as f:
            prompt = f.read()
    elif type == 4:
        with open(f"./prompts/{model}/western.txt", "r") as f:
            prompt = f.read()
    prompt = prompt.replace("[date-time]", datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S"))
    messages = await message.channel.history(limit=7).flatten()
    messages.reverse()
    response = ""
    if model == "davinci":
        for msg in messages:
            content = msg.content
            prompt += f"{msg.author} : {content}\n"
        prompt = prompt + f"{message.author}: {message.content}\nSoundy: "
        await debug(prompt)
        response = await openai.Completion.acreate(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=250,
            top_p=0.6,
            frequency_penalty=0.5,
            presence_penalty=0.2
        )
    
        response = response.choices[0].text
    
    elif model == "chatGPT":
        msgs = []
        msgs.append({"name":"System","role": "user", "content": prompt})
        name = ""
        for msg in messages:
            content = msg.content
            if msg.author.id == bot.user.id:
                role = "assistant"
                name = "assistant"
            else:
                role = "user"
                name = msg.author.name
                # The name should match '^[a-zA-Z0-9_-]{1,64}$', so we need to remove any special characters.
                name = re.sub(r"[^a-zA-Z0-9_-]", "", name)

            msgs.append({"role": role, "content": f"{content}", "name": name})
        msgs.append({"role": "user", "content": f"{message.content}", "name": message.author.name})
            
        await debug(str(msgs))
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            temperature=2,
            top_p = 0.9,
            frequency_penalty=0,
            presence_penalty=0,
            messages=msgs
        )
        
        response = response.choices[0].message.content
        
    if response == "":
        response = "I don't know what to say."
    return response
