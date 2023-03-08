import discord # to use pycord
import os # to get the token from the .env file
import openai # to use openai
from chat import response as respond # to use the response function from chat.py
from discord import default_permissions
from config import conn, c, bot
from discord.commands import option # to use options
from dotenv import load_dotenv # to load the token from a .env file
load_dotenv() # load the .env file
token = os.getenv('TOKEN') # get the token from the .env file
import asyncio
from discord.ui import Button, View 

models = ["davinci", "chatGPT"]


connections = {}
#Commands ###############################################################################################################################################################



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
    embed = discord.Embed(title="Help", description="Hello! I am Soundy, made by Pandy#0485 with the help of Paillat#7777.", color=discord.Color.blurple())
    embed.add_field(name="Commands", value="`/ping` - Responds with pong\n`/hello` - Says hello to a user\n`/help` - Shows the help message\n`/setapi`- Sets your OpenAI API key.\n`/setchannel` - Sets a channel for the bot to respond in\n`/setwelcome-/setleave` - Sets a custom welcome/leave message.\n`/setmodel` - Lets you choose the model of the chatbot.", inline=False)
    await ctx.respond(embed=embed, ephemeral=True)

channels = ["musical", "bully", "wise", "welcome", "western"]
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
    try: data = c.execute("SELECT guild_id FROM soundy WHERE guild_id = ?", (ctx.guild.id,)).fetchone()  # get the guild id from the database
    except : data = None # if the guild is not in the database, data will be None
    if data == None:
        c.execute("INSERT INTO soundy VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (str(ctx.guild.id), None, None, None, None, apikey, None, None, None)) # insert the guild id, and the api key
        conn.commit() # commit the changes
    else:
        c.execute("UPDATE soundy SET api_key = ? WHERE guild_id = ?", (apikey, str(ctx.guild.id))) # update the api key
        conn.commit() # commit the changes
    await ctx.respond("The API key has been set!", ephemeral = True) # send a message to the user

@bot.command(name="setwelcome", description="Sets the welcome message")
@default_permissions(administrator=True)
async def setwelcome(ctx, message: str):
    try: 
        c.execute("SELECT * FROM soundy WHERE guild_id = ?", (ctx.guild.id,)) # get the guild id from the database
        data = c.fetchone()
    except : data = None
    if data == None :
        c.execute("INSERT INTO soundy VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (str(ctx.guild.id), None, None, None, None, None, message, None, None)) # insert the guild id, and the api key
        conn.commit() # commit the changes
    else:
        c.execute("UPDATE soundy SET welcome_message = ? WHERE guild_id = ?", (message, str(ctx.guild.id))) # update the api key
        conn.commit()
    await ctx.respond("The welcome message has been set!", ephemeral = True) # send a message to the user
    
@bot.command(name="setleave", description="Sets the member leave message")
@default_permissions(administrator=True)
async def setleave(ctx, message: str):
    try: 
        c.execute("SELECT * FROM soundy WHERE guild_id = ?", (ctx.guild.id,)) # get the guild id from the database
        data = c.fetchone()
    except : data = None
    if data == None :
        c.execute("INSERT INTO soundy VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (str(ctx.guild.id), None, None, None, None, None, None, message, None)) # insert the guild id, and the api key
        conn.commit() # commit the changes
    else:
        c.execute("UPDATE soundy SET leave_message = ? WHERE guild_id = ?", (message, str(ctx.guild.id))) # update the api key
        conn.commit()
    await ctx.respond("The member leave message has been set!", ephemeral = True) # send a message to the user    

# Moderation Commands

@bot.command(name="ban", description="Bans a user from the server.")
@default_permissions(administrator=True)
async def ban(ctx, member: discord.Member):
    await member.ban()
    await ctx.respond(f"{member.mention} has been banned from the server!", ephemeral = True)
    
@bot.command(name="unban", description="Unbans a user from the server.")
@default_permissions(administrator=True)
async def unban(ctx, member: discord.User):
    await ctx.guild.unban(member)
    await ctx.respond(f"{member.mention} has been unbanned from the server!", ephemeral = True)
    
    
@bot.command(name="kick", description="Kicks a user from the server.")
@default_permissions(administrator=True)
async def kick(ctx, member: discord.Member):
    await member.kick()
    await ctx.responmd(f"{member.mention} has been kicked from the server!", ephemeral = True)
    
@bot.command(name="mute", description="Mutes a user from the server.")
@default_permissions(administrator=True)
async def mute(ctx, member: discord.Member):
    await member.edit(mute=True)
    await ctx.respond(f"{member.mention} has been muted from the server!", ephemeral = True)

@bot.command(name="unmute", description="Mutes a user from the server.")
@default_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
    await member.edit(mute=False)
    await ctx.respond(f"{member.mention} has been unmuted from the server!", ephemeral = True)
    
@bot.command(name="timeout", description="Times out a user from the server.")
@default_permissions(administrator=True)
async def timeout(ctx, member: discord.Member):
    await member.timeout()
    await ctx.respond(f"{member.mention} has been timed out from the server!", ephemeral = True)
    

# Set Model
async def autocomplete(ctx: discord.AutocompleteContext):
    return [model for model in models if model.startswith(ctx.value)]
@bot.command(name="setmodel", description="Select the model you want to use")
@discord.option(name="model", description="The model you want to use", required=False, autocomplete=autocomplete)
@default_permissions(administrator=True)
async def model(ctx: discord.ApplicationContext, model: str = "davinci"):
    try: 
        c.execute("SELECT * FROM model WHERE guild_id = ?", (ctx.guild.id,))
        data = c.fetchone()[1]
    except:
        data = None
    if data is None: c.execute("INSERT INTO model VALUES (?, ?)", (ctx.guild.id, model))
    else: c.execute("UPDATE model SET model_name = ? WHERE guild_id = ?", (model, ctx.guild.id))
    conn.commit()
    await ctx.respond("Model selected!", ephemeral=True)


#Events ###############################################################################################################################################################


#Member Join and Leave Events
@bot.event
async def on_member_join(member: discord.Member):
    guild = member.guild 
    try: 
        c.execute("SELECT * FROM soundy WHERE guild_id = ?", (guild.id,)) # get the guild id from the database
        data = c.fetchone()
        channel = data[4]
        try: message = data[6] 
        except: message = f"Hello {member.mention}, you are **NOT** welcome to {guild.name}!"
        if message == None: message = f"Hello {member.mention}, you are **NOT** welcome to {guild.name}!"
    except Exception as e: print(e); return
    channel = await bot.fetch_channel(channel)
    if message != f"Hello {member.mention}, you are **NOT** welcome to {guild.name}!":
        message = f"{message} {member.mention}"
    await channel.send(message)

@bot.event
async def on_member_remove(member: discord.Member):
    guild = member.guild
    try: 
        c.execute("SELECT * FROM soundy WHERE guild_id = ?", (guild.id,))
        data = c.fetchone()
        channel = data[4]
        try: message = data[7]
        except: message = f"Goodbye {member.name}, you were **not** wanted here in the first place!"
        if message == None: message = f"Goodbye {member.name}, you were **not** wanted here in the first place!"
    except Exception as e: print(e); return
    channel = await bot.fetch_channel(channel)
    if message != f"Goodbye {member.name}, you were **not** wanted here in the first place!":
        message = f"{message} {member.name}"
    await channel.send(message)
    
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
        embed = discord.Embed(title="Help", description="An unknown error occured; please try again later. If the error persists, you can contact us in our support server: https://discord.gg/zN67eGzxZC. Please send the following LOGS to the support server: ```py\n"+str(error)+"```", color=discord.Color.nitro_pink())
        await ctx.respond(embed=embed, ephemeral=True)
        
        
#Voice Channel Events  
@bot.command(name="joinvoice", description="Joins the voice channel you are in")
async def joinvoice(ctx):
    if ctx.author.voice is None: return await ctx.respond("You are not in a voice channel!", ephemeral=True)
    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.respond("Joined voice channel!", ephemeral=True)  

@bot.command(name="leavevoice", description="Leaves the voice channel it is in")
async def leavevoice(ctx):
    if ctx.guild.voice_client is None: return await ctx.respond("I am not in a voice channel!", ephemeral=True)
    await ctx.guild.voice_client.disconnect(force=True)
    await ctx.respond("Left voice channel!", ephemeral=True)     
        
@bot.event
async def on_voice_channel_leave(member: discord.Member, channel: discord.VoiceChannel):
    if member == bot.user:
        if len(channel.members) == 0:
            await channel.guild.voice_client.disconnect(force=True)
            
connections = {}

async def once_done(sink: discord.sinks, channel: discord.TextChannel, *args, ):  # Our voice client already passes these in.
    recorded_users = [  # A list of recorded users
        f"<@{user_id}>"
        for user_id, audio in sink.audio_data.items()]
    
    await sink.vc.disconnect()  # Disconnect from the voice channel.
    for user_id, audio in sink.audio_data.items():
        with open(f'./{user_id}.{sink.encoding}', 'wb+') as f:
            f.write(audio.file.read())
            f.close()
        await channel.send(f"Finished recording audio for: {', '.join(recorded_users)}.", file=discord.File(f"{user_id}.{sink.encoding}"))


@bot.command(description="Start recording")
async def record(ctx):
    noButton = Button(label="Stop Recording", style=discord.ButtonStyle.red)
    yesButton = Button(label="Record", style=discord.ButtonStyle.green)
    
    voice = ctx.author.voice
    if not voice :
        return await ctx.respond("You are not in a voice channel!", ephemeral=True)
    
    async def yesButton_callback(interaction):
        await ctx.respond("Recording...") 
        vc = await voice.channel.connect()
        connections.update({ctx.guild.id: vc})
        vc.start_recording(
        discord.sinks.WaveSink(),
        once_done,
        ctx.channel 
        )
            
    async def noButton_callback(interaction):
        if ctx.guild.id in connections:  # Check if the guild is in the cache.
            vc = connections[ctx.guild.id]
            vc.stop_recording()  # Stop recording, and call the callback (once_done).
            del connections[ctx.guild.id]  # Remove the guild from the cache.
            await ctx.delete()  # And delete.
        else:
            await ctx.respond("I am currently not recording here.")  # Respond with this if we aren't recording.

    noButton.callback = noButton_callback
    yesButton.callback = yesButton_callback    
    view = View()
    view.add_item(yesButton)
    view.add_item(noButton)
    await ctx.respond("Do you want to record?", view=view)





#On Message Events
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
    welcome_channel = data[4]
    western_channel = data[8]
    api_key = data[5]
    openai.api_key = api_key
    
    if message.author == bot.user: return
    if message.channel.id == wise_channel:
        if message.content.startswith("-"): return 
        reply = await message.reply("Thinking of wise things to say...")
        response = await respond(message,1)
        await reply.edit(response)
    
    if message.channel.id == bully_channel:
        if message.content.startswith("-"): return
        reply = await message.reply("Please stop bullying me...")
        response = await respond(message,2)
        await reply.edit(response)          
       
    if message.channel.id == music_channel:
        if message.content.startswith("-"): return
        reply = await message.reply("Ayo, thinking...")
        response = await respond(message,3)
        await reply.edit(response)      
        
    if message.channel.id == western_channel:
        if message.content.startswith("-"): return
        reply = await message.reply("Thinking partner...")
        response = await respond(message,4)
        await reply.edit(response)                

    if message.author == bot.user: return # if the message is from the bot, ignore it
    
    for o in helloes:
        if message.content.lower().find(o) != -1:
            await message.add_reaction('👋')

#Bot Events

@bot.event
async def on_ready():
    print(f'Soundy has connected to Discord!') # print the bot's name when it connects
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=f"you."))


    

bot.run(token) # runs the bot

