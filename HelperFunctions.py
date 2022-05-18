from RLTracker import *
from GoogleSheet import *

def tokenize_command(command):
	return command.lower().split(maxsplit=2)

def getPlatformLink(platform, userid):
		link = None
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
		# else:
		# 	return "Please specify platform. steam, epic, xbox, playstation, or nintendo"
		return link

async def ProcessDiscordMessage(message,discordClient, googleSheet):
	if message.author == discordClient.user:
		return

	content = message.content
	tokenized = tokenize_command(content)

	if tokenized[0] == "!rlstat":
		await RLStatCommand(tokenized, message)
		
	if tokenized[0] == "!write" and len(tokenized[1]) and len(tokenized[2]):
		await WriteCommand(tokenized, message, googleSheet)

async def RLStatCommand(blokenized, message):
	if not (len(blokenized[1]) and len(blokenized[2])):
		await message.channel.send("missing parameters.")
		await message.channel.send("!rlstat platform userid")
		return
	platform = blokenized[1]
	userid = blokenized[2]
	link = getPlatformLink(platform, userid)
	if(link == None):
		await message.channel.send("Please specify platform. steam, epic, xbox, playstation, or nintendo")

	info = rlStat(link)
	overview = PlayerOverview(info)
	embed = overview.MakeEmbed()
	await message.channel.send(embed=embed)

async def WriteCommand(blokenized, message, googleSheet):
	if not (len(blokenized[1]) and len(blokenized[2])):
		await message.channel.send("missing parameters.")
		await message.channel.send("!write platform userid")
		return
	platform = blokenized[1]
	userid = blokenized[2]
	link = getPlatformLink(platform, userid)
	if(link == None):
		await message.channel.send("Please specify platform. steam, epic, xbox, playstation, or nintendo")
	info = rlStat(link)
	overview = PlayerOverview(info)
	result = googleSheet.UpdateSheet(overview)
	if result:
		await message.channel.send("Record updated")
	else:
		await message.channel.send("Record update failed")
	