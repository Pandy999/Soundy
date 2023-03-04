import sqlite3
import logging # to log errors
import aiohttp # to make http requests
from dotenv import load_dotenv # to load the .env file
load_dotenv() # load the .env file
import os

logging.basicConfig(level=logging.INFO) # log errors

import discord
from discord import Intents # to use intents
intents = Intents.all() # to use all intents
intents.message_content = True

conn = sqlite3.connect('./data/soundy.db')
c = conn.cursor() # create a cursor
# create a table with the following values guild id, musical channel, bully channel, wise channel, general channel
c.execute('''CREATE TABLE IF NOT EXISTS soundy (guild_id text, musical_channel integer, bully_channel integer, wise_channel integer, welcome_channel integer, api_key text, welcome_message text, leave_message text,  western_channel integer)''')
c.execute('''CREATE TABLE IF NOT EXISTS model (guild_id text, model_name text)''')

bot = discord.Bot(intents=intents) # create a new bot

async def debug(message:str):
    try:
        session = aiohttp.ClientSession()
        url = os.getenv("WEBURL")
        webhook = discord.Webhook.from_url(url, session=session)
        await webhook.send(message)
    except:pass
    logging.debug(message)

