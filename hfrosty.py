import requests
import re
import ipdb
import pprint
import json
import discord

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

token = "ODgyMDM4Njk2OTA2NDY1MzEw.YS1kjA.Dwiz3G1T60gqDqAoWfKpUXMrKKM"
# https://discord.com/api/oauth2/authorize?client_id=882038696906465310&permissions=8&scope=bot

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!active teams'):
        await message.channel.send('Hello!')

client.run(token)

def getFranchiseTeams(franchiseID):
    #ipdb.set_trace()
    print("Attempting to do magic on " + franchiseID)
    host = "indy-gaming-league-api.herokuapp.com"
    s = requests.Session()
    #value = s.get('https://' + host + '/api/franchises/5fe0e1c7bce2ac0015404ffc', verify=False)
    #value = s.get('https://' + host + '/api/franchises/' + franchiseID, verify=False)
    value = s.get('https://' + host + '/api/franchises/' + franchiseID)
    object = json.loads(value.text)
    return object['franchise']['teams']

def main():
    #ipdb.set_trace()
    teams = getFranchiseTeams('5fe0e1c7bce2ac0015404ffc')
    pp = pprint.PrettyPrinter(indent=2)
    for team in teams:
        #pp.pprint(fucker)
        active = team['active']
        teamName = team['formattedName']
        teamID = team['_id']
        
        if active:
            print(f"{white}Team Name: {teamName} Team ID: {teamID}")
        else:
            print(red + teamName)

#if __name__ == "__main__":
 #   main()