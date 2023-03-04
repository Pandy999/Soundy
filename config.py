import sqlite3


conn = sqlite3.connect('./data/soundy.db')
c = conn.cursor() # create a cursor
# create a table with the following values guild id, musical channel, bully channel, wise channel, general channel
c.execute('''CREATE TABLE IF NOT EXISTS soundy (guild_id text, musical_channel integer, bully_channel integer, wise_channel integer, welcome_channel integer, api_key text, welcome_message text, leave_message text,  western_channel integer)''')
c.execute('''CREATE TABLE IF NOT EXISTS models (guild_id text, model_name text)''')