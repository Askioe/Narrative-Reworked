import sys
import os 
import random 
import discord
import subprocess
import asyncio
client = discord.Client()

token = sys.argv[1]
global text 
target = int(sys.argv[2])
delay = float(sys.argv[3])
text = str(sys.argv[4])

@client.event
async def on_ready():
    user = await client.fetch_user(target)
    while True:
        try:
            await user.send(text)
            await asyncio.sleep(delay)
        except:
            break

client.run(token, bot=False)
