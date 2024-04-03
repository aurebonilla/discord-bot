import discord
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext import commands 
from apikeys import *
import youtube_dl

intents = discord.Intents.default()  # Create instance of Intents
intents.messages = True  # Enable the message intent
intents.message_content = True  # Enable message content
cliente = commands.Bot(command_prefix= '?', intents=intents)

@cliente.event
async def on_ready():
    print('Bonilla Bot está preparado!!')
    print('----------------------')

@cliente.command()
async def hola(ctx):
    await ctx.send('Hola!! Soy Bonilla Bot y me han programado para hablarte, ¿pero no crees que es un poco raro...? ')

@cliente.command()
async def adios(ctx):
    await ctx.send('Adiós!! Fue un placer hablar contigo, espero verte pronto!!')

@cliente.command()
async def info(ctx):
    embed = discord.Embed(title="Bonilla Bot", description="Bot creado por Bonilla", color=0xeee657)
    embed.add_field(name="Autor", value="Bonilla")
    embed.add_field(name="Versión", value="1.0.0")
    embed.add_field(name="Descripción", value="Bot creado para hablar contigo")
    await ctx.send(embed=embed)

@cliente.command()
async def sumar(ctx, num1: int, num2: int):
    await ctx.send(num1 + num2)

@cliente.command()
async def restar(ctx, num1: int, num2: int):
    await ctx.send(num1 - num2)

@cliente.command()
async def multiplicar(ctx, num1: int, num2: int):
    await ctx.send(num1 * num2)

@cliente.command()
async def dividir(ctx, num1: int, num2: int):
    await ctx.send(num1 / num2)

@cliente.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(cliente.latency, 1) * 1000) + 'ms')

@cliente.command()
async def ayuda(ctx):
    embed = discord.Embed(title="Ayuda", description="Estos son los comandos de los que dispone!", color=0xeee657)
    embed.add_field(name="?hola", value="¿No crees que es raro saludar a un bot?")
    embed.add_field(name="?adios", value="Despedirte es incluso más raro que saludar...")
    embed.add_field(name="?info", value="Información del bot")
    embed.add_field(name="?sumar", value="¿Te cuesta sumar? Te ayudo!")
    embed.add_field(name="?restar", value="¿Te cuesta restar? Te ayudo!")
    embed.add_field(name="?multiplicar", value="Multplica dos números, esto lo entiendo más...")
    embed.add_field(name="?dividir", value="Divide dos números, esto lo entiendo más...")
    embed.add_field(name="?ping", value="Muestra el ping del bot")
    embed.add_field(name="?ayuda", value="Muestra los comandos disponibles")
    await ctx.send(embed=embed)

@cliente.command()
@has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member} por pesao!')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("No tienes permisos para expulsar miembros!")

@cliente.command()
@has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member} por tontoooo!')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("No tienes permisos para banear miembros!")

@cliente.command()
async def play(ctx, url : str):
    # Conectarse al canal de voz del usuario que envió el comando
    channel = ctx.message.author.voice.channel
    voice_channel = await channel.connect()

    # Usar youtube_dl para manejar la descarga del audio
    ydl_opts = {'format': 'bestaudio'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice_channel.play(discord.FFmpegPCMAudio(url2))
        await ctx.send('Reproduciendo...')

@cliente.command()
async def stop(ctx):
    voice_client = discord.utils.get(cliente.voice_clients, guild=ctx.guild)
    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send('La música se ha detenido.')
    else:
        await ctx.send('No hay música reproduciéndose en este momento.')

@cliente.command()
async def leave(ctx):
    voice_client = discord.utils.get(cliente.voice_clients, guild=ctx.guild)
    if voice_client.is_connected():
        await voice_client.disconnect()
        await ctx.send('He dejado el canal de voz.')
    else:
        await ctx.send('No estoy conectado a ningún canal de voz.')

#NO FUNCIONA AUN
@cliente.event
async def on_member_join(member: discord.Member):
    channel = cliente.get_channel(1224644022132539464)  # Reemplaza con el ID de tu canal
    await channel.send(f'Bienvenido {member.mention}! Vaya tela entrar a este servidor... si tienes alguna duda escribe "?ayuda" en el chat!')

cliente.run(token)
