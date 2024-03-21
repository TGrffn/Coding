import discord
import os
from discord.client import Client
from dotenv import load_dotenv

load_dotenv()



client = discord.Client()
token = os.getenv('token')


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == '!motivate':
        await message.channel.send(f'LETS GOOOO!!!!!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to the Knights of the Kettlebell!')



client.run(token)