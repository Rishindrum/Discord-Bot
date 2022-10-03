import json
import discord
import youtube_dl
import os
import shutil
import urllib.parse, urllib.request, re

from discord.utils import get
from os import system
from discord.ext import commands, tasks
from itertools import cycle


def get_prefix(client, message):
    with open('prefix_dictionary.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix=get_prefix)
status = cycle(['Help', 'More Help'])


@client.event
async def on_ready():
    status_change.start()
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Hello there!'))
    print('Bot\'s ready')


@client.command()
async def load(ctx, extension):
    if ctx.author.id=='263726625311424523':
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f"{extension} has been loaded.")
    else:
        await ctx.send("You are not allowed to do this.")


@client.command()
async def unload(ctx, extension):
    if ctx.author.id == '263726625311424523':
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(f"{extension} has been unloaded.")
    else:
        await ctx.send("You are not allowed to do this.")


@client.command()
async def reload(ctx, extension):
    if ctx.author.id=="263726625311424523":
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f"{extension} has been reloaded.")
    else:
        ctx.send("You are not allowed to do this.")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@tasks.loop(seconds=5)
async def status_change():
    await client.change_presence(activity=discord.Game(next(status)))



"""@client.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send('Please put in the required arguments')
    if isinstance(error, CommandNotFound):
        await ctx.send('That command does not exist bruh.')
    if isinstance(error, CheckFailure):
        await ctx.send('Can\'t do that lmao. L.')"""


client.run('NzE4OTY2NDA1NTk2MzE1Njc4.XuVX9w.5qOclNLvhpdC_btdyhPXn-V9_Ts')
