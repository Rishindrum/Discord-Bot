import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount):
        if amount.lower() == "all":
            await ctx.channel.purge()
        else:
            await ctx.channel.purge(limit=int(amount))

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} has been banned')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unban(self, ctx, *, member):
        banned_bois = await ctx.guild.bans()
        member_name, discriminator = member.split('#')
        for ban_entry in banned_bois:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.mention} has been unbanned.')

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify the amount of messages (including the one you send to clear the messages). If you want to clear all loaded messages, type all.')


def setup(client):
    client.add_cog(Moderation(client))
