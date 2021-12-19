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

print("Beginning our Journey")
class PlayerOverview:
	defaultIcon = "https://key0.cc/images/preview/11837_d71d5cb0a665b2d4e70ac7174e7929b5.png"
	platformUserHandle = None
	wins = None
	goals = None
	saves = None
	shots = None
	assists = None
	tier = None
	tierIconUrl = None
	avatarUrl = None

	def getIconUrl(self):
		if(self.avatarUrl == None):
			return self.defaultIcon
		else:
			return self.avatarUrl
	
	def __init__(self, data):
		info = data
		self.platformUserHandle = info['data']['platformInfo']['platformUserHandle']
		self.wins = info['data']['segments'][0]['stats']['wins']['value']          
		self.goals = info['data']['segments'][0]['stats']['goals']['value']          
		self.saves = info['data']['segments'][0]['stats']['saves']['value']          
		self.shots = info['data']['segments'][0]['stats']['shots']['value']          
		self.assists = info['data']['segments'][0]['stats']['assists']['value']          
		self.tier = info['data']['segments'][3]['stats']['tier']['metadata']['name']
		self.tierIconUrl = info['data']['segments'][3]['stats']['tier']['metadata']['iconUrl']
		self.avatarUrl = info['data']['platformInfo']['avatarUrl']

	def MakeEmbed(self):
		embed = discord.Embed(title="Player Overview:", colour=0xe74c3c)
		embed.set_author(name=self.platformUserHandle, icon_url=self.getIconUrl())
		embed.add_field(name="Wins:", value=self.wins, inline=True)
		embed.add_field(name="Goals:", value=self.goals, inline=True)
		embed.add_field(name="Saves:", value=self.saves, inline=True)
		embed.add_field(name="Shots:", value=self.shots, inline=True)
		embed.add_field(name="Assists:", value=self.assists, inline=True)
		embed.add_field(name="3v3 Rank:", value=self.tier, inline=False)
		embed.set_thumbnail (url=self.tierIconUrl)
		return embed


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
	return command.lower().split(maxsplit=2)

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
		userid = tokenized[2]
		if platform == "steam":
			link = "steam/" + userid
		elif platform == "epic":
			link = "epic/" + userid
		elif platform == "xbox":
			link = "xbl/" + userid
		elif platform == "nintendo":
			link = "switch/" + userid
		elif platform == "playstation":
			link == "psn/" + userid          
		else:
			await message.channel.send("Please specify platform. steam, epic, xbox, playstation, or nintendo")

		info = rlStat(link)
		overview = PlayerOverview(info)
		embed = overview.MakeEmbed()
		await message.channel.send(embed=embed)
		
client.run(token)