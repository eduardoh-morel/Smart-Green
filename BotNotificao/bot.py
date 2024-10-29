import discord
from discord.ext import commands
import asyncio
# apiKey arquivo que contem o bot_token
from apiKey import *


intents =  discord.Intents.default()
intents.message_content = True
#intents.members = True

client = commands.Bot(command_prefix='!',intents=intents)


@client.event
async def on_ready():
    print("--------------------------------------------")
    print('Bot Online')
    print(client.user.name,client.user.id)
    print("--------------------------------------------")

# Comandos gerados para testar o Bot 
@client.command(name='ola')
async def ola(ctx):
    await ctx.send('Óla estou aqui pq sim')


@client.command(name='bye')
async def bye(ctx):
    await ctx.send('Óla nao estou aqui pq eu quero')

# Bot_token esta em outro arquivo pois contem o token do bot do discord
client.run(bot_token)

