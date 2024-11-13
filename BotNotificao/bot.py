import discord
from discord.ext import commands
import asyncio
# botKey arquivo que contem o bot_token
from botKey import *

#Variaveis usadas

# Temperatura
# Verificacao sendo Feita = Temperatura Atual maior que Desejavel
temperaturaAtual = 10
temperaturaDesejada = 5
# Umidade Do Solo
# Verificacao sendo Feita = Umidade Solo Atual menor que Desejavel
umidadeSoloAtual = 0
umidadeSoloDesejada = 5
# Co2
# Verificacao sendo Feita = Co2 Atual maior que Desejavel
Co2Atual = 10
Co2Desejada = 5
# Umidade do Ar
# Verificacao sendo Feita = Umidade do Ar Atual Maior que Desejavel
umidadeArAtual = 10
umidadeArDesejada = 5


intents =  discord.Intents.default()
intents.message_content = True
#intents.members = True

client = commands.Bot(command_prefix='!',intents=intents)


@client.event
async def on_ready():
    print("--------------------------------------------")
    print('Bot Online')
    print(client.user.name, client.user.id)
    print("--------------------------------------------")
    # Iniciar as verificações de todas as condições Desejaveis
    client.loop.create_task(verificacaoTemp())
    client.loop.create_task(verificacaoUmidadeSolo())
    client.loop.create_task(verificacaoCO2())
    client.loop.create_task(verificacaoUmidadeAr())



# Verificação de Temperatura
async def verificacaoTemp():
    channel = client.get_channel(1300961217845792820)  # ID do canal onde o bot deve enviar a mensagem
    while temperaturaAtual > temperaturaDesejada: # Temperatura Atual maior que Desejavel
        embed = discord.Embed(
            title="⚠️ Alerta de Temperatura",
            description="A temperatura atual excedeu o limite desejado.",
            color=discord.Color.red()
        )
        embed.add_field(name="Temperatura Atual", value=f"{temperaturaAtual}°C", inline=True)
        embed.add_field(name="Temperatura Desejada", value=f"{temperaturaDesejada}°C", inline=True)
        embed.set_footer(text="Monitoramento de Temperatura")
        
        await channel.send(embed=embed)
        print("Verificando temperatura")
        await asyncio.sleep(5)

# Verificação de Umidade do Solo
async def verificacaoUmidadeSolo():
    channel = client.get_channel(1300961217845792820)
    while umidadeSoloAtual < umidadeSoloDesejada: # Umidade Solo Atual menor que Desejavel
        embed = discord.Embed(
            title="⚠️ Alerta de Umidade do Solo",
            description="A umidade do solo atual está abaixo do limite desejado.",
            color=discord.Color.gold()
        )
        embed.add_field(name="Umidade do Solo Atual", value=f"{umidadeSoloAtual}%", inline=True)
        embed.add_field(name="Umidade do Solo Desejada", value=f"{umidadeSoloDesejada}%", inline=True)
        embed.set_footer(text="Monitoramento de Umidade do Solo")
        
        await channel.send(embed=embed)
        print("Verificando Solo")
        await asyncio.sleep(5)

# Verificação de CO2
async def verificacaoCO2():
    channel = client.get_channel(1300961217845792820)
    while Co2Atual > Co2Desejada: # Co2 Atual maior que Desejavel
        embed = discord.Embed(
            title="⚠️ Alerta de CO2",
            description="O nível de CO2 atual está abaixo do limite desejado.",
            color=discord.Color.purple()
        )
        embed.add_field(name="CO2 Atual", value=f"{Co2Atual} ppm", inline=True)
        embed.add_field(name="CO2 Desejado", value=f"{Co2Desejada} ppm", inline=True)
        embed.set_footer(text="Monitoramento de CO2")
        
        await channel.send(embed=embed)
        await asyncio.sleep(5)

# Verificação de Umidade do Ar
async def verificacaoUmidadeAr():
    channel = client.get_channel(1300961217845792820)
    while umidadeArAtual > umidadeArDesejada: # Umidade Atual Maior que Desejavel
        embed = discord.Embed(
            title="⚠️ Alerta de Umidade do Ar",
            description="A umidade do ar atual está abaixo do limite desejado.",
            color=discord.Color.green()
        )
        embed.add_field(name="Umidade do Ar Atual", value=f"{umidadeArAtual}%", inline=True)
        embed.add_field(name="Umidade do Ar Desejada", value=f"{umidadeArDesejada}%", inline=True)
        embed.set_footer(text="Monitoramento de Umidade do Ar")
        
        await channel.send(embed=embed)
        await asyncio.sleep(5)
        

# Comandos gerados para testar o Bot 
@client.command(name='ola')
async def ola(ctx):
    await ctx.send('Óla estou aqui pq sim')


@client.command(name='bye')
async def bye(ctx):
    await ctx.send('Óla nao estou aqui pq eu quero')

# Bot_token esta em outro arquivo pois contem o token do bot do discord
client.run(bot_token)

