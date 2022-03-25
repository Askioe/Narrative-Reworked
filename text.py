import sys
import os 
import discord
import subprocess
from time import sleep
import asyncio

client = discord.Client()

token = sys.argv[1]
global text 
text = sys.argv[2]
target = int(sys.argv[3])
delay = float(sys.argv[4])


@client.event
async def on_ready():
    text = sys.argv[2]
    channel = client.get_channel(target)
    while True:
        try:
            await channel.send(text)
            await asyncio.sleep(delay)
        except:
            break

client.run(token, bot=False)
