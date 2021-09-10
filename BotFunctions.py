from discord import member
import requests
import re
import ipdb
import pprint
import json
import discord
from discord.ext import commands


black = "\033[0;30m"
red = "\033[0;31m"
green = "\033[0;32m"
yellow = "\033[0;33m"
blue = "\033[0;34m"
magenta = "\033[0;35m"
cyan = "\033[0;36m"
white = "\033[0;37m"
bright_black = "\033[0;90m"
bright_red = "\033[0;91m"
bright_green = "\033[0;92m"
bright_yellow = "\033[0;93m"
bright_blue = "\033[0;94m"
bright_magenta = "\033[0;95m"
bright_cyan = "\033[0;96m"
bright_white = "\033[0;97m"


token = "ODgyMDM4Njk2OTA2NDY1MzEw.YS1kjA.OpyCKiuBOHatcVolwjoGCJkrt6c"
host = "indy-gaming-league-api.herokuapp.com"

def getUser(userID):
	uid = userID
	s = requests.Session()
	val = s.post('https://' + host + '/api/users/' + uid, data = '{}')
	data = json.loads(val.text)
	username = data['user']['userName']
	discordId = data['user']['discordInfo']
	tracker = data['user']['rocketLeagueVerifications'][0]
	profile = username + "\n" + discordId + "\n" + tracker
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
			mystring += team['formattedName'] + " " + team['_id'] + "\n"
	return mystring


def getFranchiseTeams(franchiseID):
	#ipdb.set_trace()
	print("Attempting to do magic on " + franchiseID)
	s = requests.Session()
	value = s.get('https://' + host + '/api/franchises/' + franchiseID)
	object = json.loads(value.text)
	return object['franchise']['teams']

# https://discord.com/api/oauth2/authorize?client_id=882038696906465310&permissions=8&scope=bot

client = discord.Client()

def getTeam(teamID):
	s = requests.Session()
	val = s.get('https://' + host + '/api/teams/' + teamID)
	data = json.loads(val.text)
	info = ""
	for i in data['team']['players']:
		info += i["userName"] + " " + i["id"] + "\n"
	return info

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
		await message.channel.send(info)

	if tokenized[0] == '!teams':
		await message.channel.send(getActiveTeams())

	if tokenized[0] == "!playerstat" and len(tokenized[1]):
		profile = getPlayerName(tokenized[1])
		await message.channel.send(profile)

	# if content.startswith('!stats'):
	# 	await message.channel.send("Initializing stat request")
	
	if content.startswith('!rank'):
		await message.channel.send("your rank is garbage.")
	
	if content.startswith('!playerlist'):
		await message.channel.send(getPlayerName())


#client  = commands.Bot(command_prefix='!')


# @client.command()
# async def teamstat(ctx, *, arg):
# 	await ctx.send(shiftystat(arg))

# @client.command()
# async def kick(ctx, member : discord.Member, *, reason=None):
# 	await member.kick(reason=reason)

# @client.command()
# async def ban(ctx, member : discord.Member, *, reason=None):
# 	await member.ban(reason=reason)

# @client.command()
# async def invites(ctx, usr: discord.Member=None):
#     if usr == None:
#        user = ctx.author
#     else:
#        user = usr
#     total_invites = 0
#     for i in await ctx.guild.invites():
#         if i.inviter == user:
#             total_invites += i.uses
#     await ctx.send(f"{user.name} has invited {total_invites} member{'' if total_invites == 1 else 's'}!")

client.run(token)

# def main():
# 	#ipdb.set_trace()
# 	shifty = getUser('5fe033b3bce2ac0015402e50')
# 	teams = getFranchiseTeams('5fe0e1c7bce2ac0015404ffc')
# 	#pp = pprint.PrettyPrinter(indent=2)
# 	for team in teams:
# 		#pp.pprint(fucker)
# 		active = team['active']
# 		teamName = team['formattedName']
# 		teamID = team['_id']

# 		if active:
# 			print(f"{white}Team Name: {teamName} Team ID: {teamID}")
# 		else:
# 			print(red + teamName)

# main()