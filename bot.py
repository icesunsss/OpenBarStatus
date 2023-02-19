# bot.py
import os

import discord
from discord.ext import commands
intents = discord.Intents.all()

from dotenv import load_dotenv

from urllib.request import urlopen
import json
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
serverIP_1 = os.getenv('SERVER_IP_1')
serverIP_2 = os.getenv('SERVER_IP_2')

serverIP = serverIP_1 + ":" + serverIP_2
serverstatus_url = "https://api.mcsrvstat.us/2/" + serverIP

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == 'serverstatus':
        request = urlopen(serverstatus_url)
        data_json = json.loads(request.read())
        server_status = data_json
        if server_status['online']:
            nb_players = server_status['players']['online']
            if nb_players > 1:
                players = server_status['players']['list']
                response = "Le serveur est en ligne avec " + str(nb_players) + " joueurs connectés : " + ", ".join(players)
            elif nb_players == 1 :
                response = "Le serveur est en ligne avec 1 joueur connecté : " + players[0]
            else :
                response = "Le serveur est en ligne, aucun joueur n'est connecté"
        else :
            response = "Le serveur est down, Nolly à l'aide"
        await message.channel.send(response)

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='server', help='Get status information of openbar-galactique.thenolle.com')
async def status(ctx):
    request = urlopen(serverstatus_url)
    data_json = json.loads(request.read())
    server_status = data_json
    if server_status['online']:
        #print(server_status)
        nb_players = server_status['players']['online']
        if nb_players > 1:
            players = server_status['players']['list']
            response = "Le serveur est en ligne avec " + str(nb_players) + " joueurs connectés : " + ", ".join(players)
        elif nb_players == 1 :
            players = server_status['players']['list']
            response = "Le serveur est en ligne avec 1 joueur connecté : " + players[0]
        else :
            response = "Le serveur est en ligne, aucun joueur n'est connecté"
    else :
        response = "Le serveur est down, <@553628781156237313> à l'aide"
    await ctx.send(response)

bot.run(TOKEN)

