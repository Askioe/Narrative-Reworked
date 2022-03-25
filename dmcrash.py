import sys
import os 
import random 
import discord
import subprocess
import asyncio
from time import sleep
client = discord.Client()

token = sys.argv[1]
target = int(sys.argv[2])
delay = float(sys.argv[3])


@client.event
async def on_ready():
    text = ":chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains: :chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains: :chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains: :chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains:"
    user = await client.fetch_user(target)
    while True:
        try:
            await user.send(text)
            await asyncio.sleep(delay)
        except:
            break

client.run(token, bot=False)