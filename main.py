import discord # to use pycord
import os # to get the token from the .env file
import logging # to log errors
import openai # to use openai
from chat import chatgpt_response
from chat2 import chatgpt_response2
from chat3 import chatgpt_response3
import sqlite3
from discord import default_permissions

conn = sqlite3.connect('soundy.db')
c = conn.cursor() # create a cursor
# create a table with the following values guild id, musical channel, bully channel, wise channel, general channel
c.execute('''CREATE TABLE IF NOT EXISTS soundy (guild_id text, musical_channel integer, bully_channel integer, wise_channel integer, welcome_channel integer, api_key text)''')


from discord import Intents # to use intents
intents = Intents.all() # to use all intents
intents.message_content = True

logging.basicConfig(level=logging.INFO) # log errors

from discord.commands import option # to use options

from dotenv import load_dotenv # to load the token from a .env file
load_dotenv() # load the .env file
token = os.getenv('TOKEN') # get the token from the .env file
openai_apikey = os.getenv('OPENAI_APIKEY')



#Commands ###############################################################################################################################################################


bot = discord.Bot(intents=intents) # create a new bot

#Ping Command
@bot.command(name='ping', description='Responds with pong') # name and description are optional
async def ping(ctx): # answer with the ping
    await ctx.respond(f'Pong! {round(bot.latency * 1000)}ms', ephemeral=True) # ephemeral=True makes the message only visible to the user

#Hello Command
@bot.command(name='hello', description='Says hello to a user') # name and description are optional
@option(name='your name', description='Your name', required=False) # required=True makes the option required
async def hello(ctx, your_name:str = ""): # say hello to the user
    await ctx.respond(f'Hello {your_name}!', ephemeral=True) # ephemeral=True makes the message only visible to the user. f means that you can use {} to insert variables

#Help Command
@bot.command(name='help', description='Shows the help message') # name and description are optional
async def ping(ctx):
   # await ctx.respond(f'Hello! I am a bot made by Pandy#0485. I am currently in development, so I don\'t have many commands.', ephemeral=True)
    embed = discord.Embed(title="Help", description="Hello! I am a bot made by Pandy#0485 with the help of Paillat#7777.", color=discord.Color.nitro_pink())
    embed.add_field(name="Commands", value="`/ping` - Responds with pong\n`/hello` - Says hello to a user\n`/help` - Shows the help message", inline=False)
    await ctx.respond(embed=embed, ephemeral=True)

channels = ["musical", "bully", "wise", "welcome"]
async def get_channel(ctx: discord.AutocompleteContext):
    return [channel_name for channel_name in channels if channel_name.startswith(ctx.value)]

@bot.command(name="setchannel", description="Sets a channel for the bot to respond in")
@discord.commands.option(name="scope", description="The type of channel", autocomplete=get_channel)
@discord.commands.option(name="channel", description="The channel to set")
@default_permissions(administrator=True)
async def setchannel(ctx, scope: str, channel: discord.TextChannel):
    try: 
        c.execute("SELECT * FROM soundy WHERE guild_id = ?", (ctx.guild.id,)) # get the guild id from the database
        data = c.fetchone()
    except : data = None
    if data == None or data[5] == None:
        await ctx.respond("You need to set an API key first!")
        return
#now we know that the guild is in the database, so we update the channel
    c.execute(f"UPDATE soundy SET {scope}_channel = ? WHERE guild_id = ?", (channel.id, ctx.guild.id))
    conn.commit()
    await ctx.respond(f"The {scope} channel has been set to {channel.mention}")
    
    
@bot.command(name="setapi", description="Sets the OpenAI API key")
@default_permissions(administrator=True)
async def setapi(ctx, apikey: str):     
    try: data = c.execute("SELECT guild_id FROM soundy WHERE guild_id = ?", (ctx.guild.id,)).fetchone()  #
    except : data = None # if the guild is not in the database, data will be None
    if data == None:
        c.execute("INSERT INTO soundy VALUES (?, ?, ?, ?, ?, ?)", (str(ctx.guild.id), None, None, None, None, apikey)) # insert the guild id, and the api key
        conn.commit() # commit the changes
        await ctx.respond("The API key has been set!", ephemeral = True) # send a message to the user
    else:
        c.execute("UPDATE soundy SET api_key = ? WHERE guild_id = ?", (apikey, str(ctx.guild.id))) # update the api key
        conn.commit() # commit the changes
        await ctx.respond("The API key has been set!", ephemeral = True) # send a message to the user



#Events ###############################################################################################################################################################


#Member Join and Leave Events
@bot.event
async def on_member_join(member: discord.Member):
    guild = member.guild
    try: 
        c.execute("SELECT * FROM soundy WHERE guild_id = ?", (guild.id,))
        data = c.fetchone()
        channel = data[4]
    except : return
    channel = await bot.fetch_channel(channel)
    await channel.send(f"Hello {member.mention}, you are **NOT** welcome to {guild.name}!")

@bot.event
async def on_member_leave(member: discord.Member):
    guild = member.guild
    try: 
        c.execute("SELECT * FROM soundy WHERE guild_id = ?", (guild.id,))
        data = c.fetchone()
        channel = data[4]
    except : return
    channel = await bot.fetch_channel(channel)
    await channel.send(f"Goodbye {member.name}, you were **not** wanted here in the first place!")
    
@bot.event
#when the bot is added to a new server, we want to send a message to the user who added the bot to the server
async def on_guild_join(guild: discord.Guild):
    #we get the audit log entry of the bot being added to the server
    audit_log_entry = await guild.audit_logs(limit=1, action=discord.AuditLogAction.bot_add).flatten()
    #we get the user who added the bot to the server
    user = audit_log_entry[0].user
    #we send a message to the user who added the bot to the server
    await user.send(f"") #Here a message explaining how to use and setup the server, and that they have 18$ free with openai but then it's paid, and where to find an api key

@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: Exception):
    if str(error) == "Application Command raised an exception: Forbidden: 403 Forbidden (error code: 50013): Missing Permissions":
        await ctx.respond("I don't have the permissions to do that", ephemeral=True)
    else:   
        await ctx.respond("An unknown error occured; please try again later. If the error persists, you can contact us in our support server: https://discord.gg/Psdxy69ZQn. Please send the following LOGS to the support server: \`\`\`py\n"+str(error)+"\`\`\`", ephemeral=True)
        print(error)


#On Message Events

banned_words = ["carpet"]
helloes = ["hello", "hi", "hey"]

@bot.event
async def on_message(message):
    try: guild_id = str(message.guild.id)
    except: return
    try: 
        c.execute("SELECT * FROM soundy WHERE guild_id = ?", (guild_id,))
        data = c.fetchone()
    except: data = None
    if data is None: return
    music_channel = data[1]
    bully_channel = data[2]
    wise_channel = data[3]
    general_channel = data[4]
    api_key = data[5]
    openai.api_key = api_key
    
    if message.author == bot.user: return
    if message.channel.id == wise_channel:
        if message.content.startswith("-"): return 
        reply = await message.reply("Thinking of wise things to say...")
        response = await chatgpt_response(message.content)
        await reply.edit(response)
    
    if message.channel.id == bully_channel:
        if message.content.startswith("-"): return
        reply = await message.reply("Please stop bullying me...")
        response = await chatgpt_response2(message.content)
        await reply.edit(response)          
       
    if message.channel.id == music_channel:
        if message.content.startswith("-"): return
        reply = await message.reply("Ayo, thinking...")
        response = await chatgpt_response3(message.content)
        await reply.edit(response)                   
    
    for i in banned_words:
        if message.content.lower().find(i) != -1:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, I'm gonna have to wash your tongue with soap!")

    if message.author == bot.user: return # if the message is from the bot, ignore it
    
    for o in helloes:
        if message.content.lower().find(o) != -1:
            await message.add_reaction('👋')


#Bot Events

@bot.event
async def on_ready():
    print(f'Soundy has connected to Discord!') # print the bot's name when it connects
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=f"you."))
    channel = await bot.fetch_channel(1072806328524869715)
    await channel.send(f"Heh, I'm back boys.")


    

bot.run(token) # runs the bot