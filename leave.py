import sys
import os 
import random 
import discord
import subprocess
from time import sleep
import asyncio
client = discord.Client()

token = sys.argv[1]
server = int(sys.argv[2])


@client.event
async def on_ready():
    guild = client.get_guild(server)
    if guild is None:
        sys.exit()
    await guild.leave()
    await asyncio.sleep(.1)
    sys.exit()


client.run(token, bot=False)