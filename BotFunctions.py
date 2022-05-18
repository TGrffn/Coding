import discord
from configparser import ConfigParser
from RLTracker import *
from HelperFunctions import *
from GoogleSheet import *



print("Beginning our Journey")
parser = ConfigParser()
parser.read('SlothSteveToken.ini')
discordtoken = parser.get('BotToken', 'token')
googleSheetsKey = parser.get('GoogleSheets', 'key')
googleSheet = UpdateSheet(googleSheetsKey)
client = discord.Client()

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	await ProcessDiscordMessage(message, client, googleSheet)

client.run(discordtoken)