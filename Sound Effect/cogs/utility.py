import discord
import json
from discord.ext import commands


async def update_data(users, user, guild):
    if str(guild) not in users:
        users[str(guild)] = {}
    if str(user.id) not in users[str(guild)]:
        users[str(guild)][str(user.id)] = {}
        users[str(guild)][str(user.id)]['experience'] = 0
        users[str(guild)][str(user.id)]['level'] = 1


async def add_experience(users, user, exp, guild):
    users[str(guild)][str(user.id)]['experience'] += exp


async def level_up(users, user, channel, guild):
    experience = users[str(guild)][str(user.id)]['experience']
    lvl_start = users[str(guild)][str(user.id)]['level']
    level_end = int(experience ** (1/4))

    if lvl_start < level_end:
        await channel.send(f'{user.mention} has leveled up to {level_end}')
        users[str(guild)][str(user.id)]['level'] = level_end


class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('prefix_dictionary.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = '.'

        with open('prefix_dictionary.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('prefix_dictionary.json', 'r') as f:
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open('prefix_dictionary.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.command()
    async def changeprefix(self, ctx, prefix):
        with open('prefix_dictionary.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('prefix_dictionary.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        await ctx.send(f'Prefix changed to {prefix}')

    @commands.command(aliases=['ech', 'e', 'E', "Ech", 'Echo'])
    async def echo(self, ctx, echo):
        await ctx.send(echo)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        for channel in member.guild.channels:
            if str(channel) == 'general':
                await channel.send(f'Welcome to the server {member.mention}')
        print(f"{member} has joined the server.")
        with open('users.json', 'r') as f:
            users = json.load(f)

        await update_data(users, member)

        with open('users.json', 'w') as f:
            json.dump(users, f)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} has left the server.')

    @commands.command(aliases=['Ping'])
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency*1000)} ms')

    @commands.Cog.listener()
    async def on_message(self, message):
        with open('users.json', 'r') as f:
            users = json.load(f)
        if not message.author.bot:
            await update_data(users, message.author, message.guild.id)
            await add_experience(users, message.author, 5, message.guild.id)
            await level_up(users, message.author, message.channel, message.guild.id)

        with open('users.json', 'w') as f:
            json.dump(users, f)
        id = self.client.get_guild(message.guild.id)
        channels = ['commands']
        valid_users = ["Rishdra#5449"]
        #if str(message.channel) in channels and str(message.author) in valid_users:>>>For ones you want in specific channel


    #IF SOMEONE SAYS IM ___ THE BOT SAYS HI AND GREETS ITSELF
        if not message.author.bot:

            if message.content.lower().find('im ') != -1 and (message.content.lower()[message.content.lower().find('im')-1] == ' ' or message.content.lower().find('im') == 0):
                name=message.content.lower()[message.content.lower().find('im ')+3 : len(message.content)+1]
                await message.channel.send("Hi "+name+", my name is Sound Effect bot! It was very nice meeting you!")

            elif message.content.lower().find("i'm ") != -1 and (message.content.lower()[message.content.lower().find("i'm")-1] == ' ' or message.content.lower().find("i'm") == 0):
                name=message.content.lower()[message.content.lower().find("i'm ")+4 : len(message.content)+1]
                await message.channel.send("Hi "+name+", my name is Sound Effect bot! It was very nice meeting you!")

            elif message.content.lower().find("i am ") != -1 and (message.content.lower()[message.content.lower().find("i am")-1] == ' ' or message.content.lower().find("i am") == 0):
                name=message.content.lower()[message.content.lower().find("i am ")+5 : len(message.content)+1]
                await message.channel.send("Hi "+name+", my name is Sound Effect bot! It was very nice meeting you!")

        #IF SOMEONE SAYS MEMBERS THEN THE AMOUNT OF MEMBERS WILL return

            elif message.content.find('MEMBERS') != -1:
                await message.channel.send(f"There are {id.member_count} members in this server!")


def setup(client):
    client.add_cog(Utility(client))
