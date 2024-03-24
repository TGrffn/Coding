import discord
import os
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()
intents = discord.Intents.all()
token = os.getenv('token')

@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!motivate'):
        embed = discord.Embed(title="Stay Motivated", description="Keep Pushing! You've got this!", color=0xFF5733)
        await message.channel.send(embed = embed)

client.run(token)