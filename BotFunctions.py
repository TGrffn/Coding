from os import name
from discord import colour, member
import requests
import re
import ipdb
import pprint
import json
import discord
from discord.ext import commands
from configparser import ConfigParser



parser = ConfigParser()
parser.read('SlothSteveToken.ini')

token = parser.get('BotToken', 'token')
		
def rlStat(link):
	endpoint = link
	url = 'https://api.tracker.gg/api/v2/rocket-league/standard/profile/' + endpoint
	s = requests.Session()
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
	}
	vdata = s.get(url, headers=headers)
	name = json.loads(vdata.text)
	return name	

client = discord.Client()

def tokenize_command(command):
	return command.lower().split(maxsplit=1)

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	content = message.content
	tokenized = tokenize_command(content)

	if tokenized[0] == "!rlstat" and len(tokenized[1]) and len(tokenized[2]):
		platform = tokenized[1]
		link = ""
		if platform == "steam":
			link = "steam/" + tokenized[2]
		else:
			if platform == "epic":
				link = "epic/" + tokenized[2]
			else:
				if platform == "xbox":
					link = "xbl/" + tokenized[2]
				else:
					if platform == "nintendo":
						link = "switch/" + tokenized[2]
					else:
						if platform == "playstation":
							link == "psn/" + tokenized[2]
						else:
							await message.channel.send("Please specify platform. steam, epic, xbox, playstation, or nintendo")

		info = rlStat(link)
		embed = discord.Embed(title="Player Overview:", colour=0xe74c3c)
		embed.set_author     (name=info['data']['platformInfo']['platformUserHandle'], icon_url='https://key0.cc/images/preview/463_eb72c1e7f13edc624aa5f6372112e001.png')
		embed.add_field      (name="Wins:",     value=info   ['data']['segments'][0]['stats']['wins']   ['value'],            inline=True)
		embed.add_field      (name="Goals:",    value=info   ['data']['segments'][0]['stats']['goals']  ['value'],            inline=True)
		embed.add_field      (name="Saves:",    value=info   ['data']['segments'][0]['stats']['saves']  ['value'],            inline=True)
		embed.add_field      (name="Shots:",    value=info   ['data']['segments'][0]['stats']['shots']  ['value'],            inline=True)
		embed.add_field      (name="Assists:",  value=info   ['data']['segments'][0]['stats']['assists']['value'],            inline=True)
		embed.add_field      (name="3v3 Rank:", value=info   ['data']['segments'][3]['stats']['tier']   ['metadata']['name'], inline=False)
		embed.set_thumbnail  (url=info['data']['segments'][3]['stats']['tier']['metadata']['iconUrl'])
		await message.channel.send(embed=embed)

	
client.run(token)