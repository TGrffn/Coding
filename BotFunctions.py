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

host = "indy-gaming-league-api.herokuapp.com"


def getUser(userID):
	uid = userID
	s = requests.Session()
	val = s.post('https://' + host + '/api/users/' + uid, data = '{}')
	data = json.loads(val.text)
	profile = data
	return profile

def getPlayerName(id):
	data = getActiveInfo()
	name = id
	playerlist = ""
	for n in data['franchise']['playerIds']:
		if name == n["userName"].lower():
			playerlist += n["_id"]
	profiles = getUser(playerlist)
	return profiles

def getPlayerList():
	data = getActiveInfo()
	players = ""
	for i in data['franchise']['playerIds']:
		players += i["userName"] + "\n"
	return players


def getActiveInfo():
	s = requests.Session()
	val = s.get('https://' + host + '/api/franchises/' + '5fe0e1c7bce2ac0015404ffc')
	data = json.loads(val.text)
	return data


def getActiveTeams():
	fid = '5fe0e1c7bce2ac0015404ffc'
	values = getFranchiseTeams(fid)
	mystring = ""
	for team in values:
		if team['active']:
			mystring += team['formattedName'] + "\n"
	return mystring


def getFranchiseTeams(franchiseID):
	print("Attempting to do magic on " + franchiseID)
	s = requests.Session()
	value = s.get('https://' + host + '/api/franchises/' + franchiseID)
	object = json.loads(value.text)
	return object['franchise']['teams']


client = discord.Client()

def getTeam(teamID):
	s = requests.Session()
	val = s.get('https://' + host + '/api/teams/' + teamID)
	team = json.loads(val.text)
	return team

def teamstat(stat):
	tname = getActiveInfo()
	name = stat
	myString = ""
	for n in tname['franchise']['teams']:
		if n['active']:
			if n['__v'] > 0:
				if name == n['formattedName'].lower():
					myString += n['_id']
					break
	info = getTeam(myString)
	return info
		
	

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

	if tokenized[0] == "!teamstat" and len(tokenized[1]):
		info = teamstat(tokenized[1])
		pname = ""
		for i in info['team']['players']:
			pname += i["userName"] + "\n"
		embed = discord.Embed(title="Team Info", description=info['team']['circuitName'], colour=0xe74c3c)
		embed.set_author(name="SlothSqua", url="https://www.indygamingleague.com/franchises/5fe0e1c7bce2ac0015404ffc", icon_url="https://pbs.twimg.com/profile_images/1397976693650886658/SJjDTS6N_400x400.jpg")
		embed.add_field(name="Team Name:", value=info['team']['formattedName'], inline=False)
		embed.add_field(name="Captain:", value=info['team']['captain']['userName'], inline=True)
		embed.add_field(name="Players:", value=pname, inline=True)
		await message.channel.send(embed=embed)

	if tokenized[0] == '!teams':
		i = getActiveTeams()
		embed = discord.Embed(title="Active Team List:", description=i, colour=0x2ecc71)
		embed.set_author(name="SlothSqua", url="https://www.indygamingleague.com/franchises/5fe0e1c7bce2ac0015404ffc", icon_url="https://pbs.twimg.com/profile_images/1397976693650886658/SJjDTS6N_400x400.jpg")
		await message.channel.send(embed = embed)

	if tokenized[0] == "!playerstat" and len(tokenized[1]):
		profile = getPlayerName(tokenized[1])
		link = profile['user']['rocketLeagueVerifications'][0]
		embed = discord.Embed(title="Player Profile", colour=0x87CEEB)
		embed.set_author(name="SlothSqua", url="https://www.indygamingleague.com/franchises/5fe0e1c7bce2ac0015404ffc", icon_url="https://pbs.twimg.com/profile_images/1397976693650886658/SJjDTS6N_400x400.jpg")
		embed.add_field(name="Player Name:", value=profile['user']['userName'], inline=True)
		embed.add_field(name="Discord:", value=profile['user']['discordInfo'],inline=True)
		embed.add_field(name="Rocket League Tracker:", value=link, inline=False)
		embed.set_thumbnail(url="https://wallpaperaccess.com/full/5089224.jpg")
		await message.channel.send(embed=embed)
	
	if content.startswith('!rank'):
		embed = discord.Embed(title="Hello, world!", description=":D", colour=0x87CEEB)
		await message.channel.send(embed = embed)
	
	if content.startswith('!playerlist'):
		await message.channel.send(getPlayerList())
	


client.run(token)