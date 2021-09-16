from os import name
from discord import colour, member
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

# https://discord.com/api/oauth2/authorize?client_id=882038696906465310&permissions=8&scope=bot

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
		# link2 = profile['user']['rocketLeagueVerifications'][1]
		embed = discord.Embed(title="Player Profile", colour=0x87CEEB)
		embed.set_author(name="SlothSqua", url="https://www.indygamingleague.com/franchises/5fe0e1c7bce2ac0015404ffc", icon_url="https://pbs.twimg.com/profile_images/1397976693650886658/SJjDTS6N_400x400.jpg")
		embed.add_field(name="Player Name:", value=profile['user']['userName'], inline=True)
		embed.add_field(name="Discord:", value=profile['user']['discordInfo'],inline=True)
		embed.add_field(name="Rocket League Tracker:", value=link, inline=False)
		embed.set_thumbnail(url="https://wallpaperaccess.com/full/5089224.jpg")
		await message.channel.send(embed=embed)

	# if content.startswith('!stats'):
	# 	await message.channel.send("Initializing stat request")
	
	if content.startswith('!rank'):
		embed = discord.Embed(title="Hello, world!", description=":D", colour=0x87CEEB)
		await message.channel.send(embed = embed)
	
	if content.startswith('!playerlist'):
		await message.channel.send(getPlayerList())
	


# client  = commands.Bot(command_prefix='!')

# @client.command()
# async def clear(ctx, amount = int):
# 	await ctx.channel.purge(limit = amount)

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

# # function Get-TrackerData(){
# #     param([string]$ID, [Switch]$Steam, [Switch]$Epic, [switch]$Xbox, [switch]$Playstation, [switch]$Nintendo)
# #     $endpoint = ""
# #     if($Steam){
# #         $endpoint = "steam/$ID"
# #         #Example-Squishy: "steam/76561198286759507"  # "steam/SquishyMuffinz" # Does this work??  ## YES..
# #     }
# #     elseif($Epic){
# #         $endpoint = "epic/$ID" # "epic/RealLethamyr" #force return leth  # "epic/sh1ftybit" (main epic account)  # "epic/shiftybit"(nintendo switch epic smurf) 
# #     }
# #     elseif($xbox){
# #         $endpoint =  "xbl/$id" #"xbl/wolfbyt3" # returns my xbox account (linked to my epic so this is the same as my steam)
# #     }
# #     elseif($Playstation){
# #         $endpoint = "psn/$id" # "psn/First-Killer-19" # returns firstkiller on playstation. 
# #     }
# #     elseif($Nintendo) { # $Switch is not a good var name, it's a keyword in many langs. I pick $Nintendo
# #         $endpoint = "switch/$id"   # "switch/Nuqqet" # this is the #1 switch player on leaderboards
# #     }
# #     else{
# #         Write-Error "Please specify platform. -Steam, -Epic, -Xbox, -Playstation, or -Nintendo"
# #         return
# #     }
# #     $json = (curl "https://api.tracker.gg/api/v2/rocket-league/standard/profile/$endpoint").content
# #     $data = ($json | ConvertFrom-Json).Data
# #     return $data
# # }
# # function DetailView(){
# #     param($in)
# #     $playlists = $in.segments| ?{$_.type -eq "playlist"} 
# #     foreach($playlist in $playlists){
# #         $Percentile = 100 - $playlist.stats.rating.percentile
# #         [PSCustomObject] @{
# #             "Playlist" = $playlist.metadata.name;
# #             #"Tier" = $playlist.stats.tier.value; #number. 0 is bronze 1, 3 is silver 1, 4 is silver 2, etc. 
# #             "MMR" =  $playlist.stats.rating.value;
# #             #"Rank" = $playlist.stats.tier.metadata.name;
# #             "Rank" = "$($playlist.stats.tier.metadata.name) div $($playlist.stats.division.value)." #Friendly Rank 
# #             #"Division" = $playlist.stats.division.metadata.name;
# #             "SeasonMatches" = $playlist.stats.matchesPlayed.value;
# #             "Percentile" = "top $Percentile%";

# #         }
# #     }
# #     #$playlists | %{"$($_.metadata.name) - $($_.stats.tier.value) "} 
# # }
# # function overview(){
# #     param($in)
# #     $overview = $in.segments[0].stats
# #     [PSCustomObject]@{
# #         Wins = $overview.wins.value;
# #         Goals = $overview.goals.value;
# #         Shots = $overview.shots.value;
# #         MVPs = $overview.mvps.value;
# #         Saves = $overview.saves.value;
# #         Assists = $overview.assists.value;
# #     }
# # }