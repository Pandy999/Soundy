import discord
import os
import logging

logging.basicConfig(level=logging.INFO) # log errors

from dotenv import load_dotenv # to load the token from a .env file
load_dotenv() # load the .env file
token = os.getenv('TOKEN') # get the token from the .env file

intents = discord.Intents.default()
intents.members = True  # This intent requires "Server Member Intent" to be enabled at https://discord.com/developers
# ^ This may give you `read-only` warning, just ignore it.

bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    print("Ready!")



bot.run(token)