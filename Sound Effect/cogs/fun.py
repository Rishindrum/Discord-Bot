import random
import discord
import json
import praw
from random import randint
from discord.ext import commands


async def update_d(users, user, guild):
    if str(guild) not in users:
        users[str(guild)] = {}
        if str(user.id) not in users[str(guild)]:
            users[str(guild)][str(user.id)] = {}
            users[str(guild)][str(user.id)]['wins'] = 0


async def add_wins(users, user, win, guild):
    users[str(guild)][str(user.id)]['wins'] += win
    global wins
    wins = users[str(guild)][str(user.id)]['wins']

reddit = praw.Reddit(client_id='DsuOibOw2Sn8nw',
                         client_secret='kbysTLH6ktX7xM6lqRmmD7bU1rw',
                         user_agent='windows:discord:v3.8.3 (by u/Rindra_Dalundri)')


async def submi(image):
    memes_submissions = reddit.subreddit(str(image)).hot()
    post_to_pick = random.randint(1, 10)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)
    if str(submission.url).endswith('.png') or str(submission.url).endswith('.jpg'):
        return submission.url
    else:
        submi(image)


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    def custom(ctx):
        return ctx.author.id == 263726625311424523

    @commands.command()
    async def reddit(self, ctx, image):
        memes_submissions = reddit.subreddit(str(image)).hot()
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
        await ctx.send(submission.url)
        #if str(submission.url).endswith('.png') or str(submission.url).endswith('.jpg'):
         #   await ctx.send(submission.url)
        #else:
         #   await ctx.send(submi(image))

    @commands.command()
    @commands.check(custom)
    async def cool(self, ctx):
        await ctx.send(f'{ctx.author} is the coolest one over here.')

    @commands.command()
    async def meme(self, ctx):
        num = randint(0, 3)
        try:
            await ctx.send(file=discord.File("MEMES/{}.jpg".format(num)))
        except:
            await ctx.send(file=discord.File("MEMES/{}.png".format(num)))

    @commands.Cog.listener()
    async def on_member_join(self, member):

        with open('rps.json', 'r') as f:
            rps = json.load(f)

        await update_d(rps, member)

        with open('rps.json', 'w') as f:
            json.dump(rps, f)

    @commands.command(aliases=['rps', 'RPS'])
    async def rock_paper_scissors(self, ctx, move):
        with open('rps.json', 'r') as f:
            rps = json.load(f)

        embed = discord.Embed(
            color=discord.Colour.blue(),
            title='Rock Paper Scissors!'
        )
        response = ['rock', 'paper', 'scissors']
        your_move = str(move).lower()
        win = 0
        if your_move in response:
            bot_move = random.choice(response)
            if (your_move == 'rock' and bot_move == 'scissors') or (
                    your_move == 'scissors' and bot_move == 'paper') or (your_move == 'paper' and bot_move == 'rock'):
                embed.set_author(name="WINNER!",
                                 icon_url="https://media.discordapp.net/attachments/718975206319718424/7204271725519832"
                                          "04/M-spgx7lE5adbuR7zgeFWJ3PCVsNAvX7phd8vedUsn-h9b5DsyYen8-BQHGUdexMSTooGE0Cf"
                                          "f87RLg_RUE8j5ioXnqc64Z77WYZ.png")
                embed.set_image(
                    url="https://media.discordapp.net/attachments/718975206319718424/720429270408626316/giphy.png")
                await ctx.send(f'You choose {your_move}.')
                await ctx.send(file=discord.File(f"RPS/{your_move}.jpg"))
                await ctx.send(f'I choose {bot_move}.')
                await ctx.send(file=discord.File(f"RPS/{bot_move}.jpg"))
                win += 1
            elif your_move == bot_move:
                embed.set_author(name="TIE!",
                                 icon_url="https://cdn.discordapp.com/attachments/718975206319718424/720427465650077706"
                                          "/cdf4de6dac8f6dbae1b1f69008cc3b3b.png")
                embed.set_image(
                    url="https://cdn.discordapp.com/attachments/718975206319718424/720464427912265758/l-29994-hold-up-w"
                        "e-was-tied.png")
                await ctx.send(f'You choose {your_move}.')
                await ctx.send(file=discord.File(f"RPS/{your_move}.jpg"))
                await ctx.send(f'I choose {bot_move}.')
                await ctx.send(file=discord.File(f"RPS/{bot_move}.jpg"))
            else:
                embed.set_author(name="LOSER!",
                                 icon_url="https://cdn.discordapp.com/attachments/718975206319718424/720427781967708240"
                                          "/free-lisa-simpson-l-for-loser-the-simpsons-enamel-pin-just-pay-shipping_gra"
                                          "nde.png")
                embed.set_image(
                    url="https://cdn.discordapp.com/attachments/718975206319718424/720463863161684058/2va6u8.png")
                await ctx.send(f'You choose {your_move}.')
                await ctx.send(file=discord.File(f"RPS/{your_move}.jpg"))
                await ctx.send(f'I choose {bot_move}.')
                await ctx.send(file=discord.File(f"RPS/{bot_move}.jpg"))

            await update_d(rps, ctx.author, ctx.guild.id)
            await add_wins(rps, ctx.author, win, ctx.guild.id)

            with open('rps.json', 'w') as f:
                json.dump(rps, f)
            embed.add_field(name='WIN COUNT', value=f'{ctx.author} has {wins} wins', inline=False)
            embed.set_footer(text="Play again if you want another win!")
            await ctx.send(embed=embed)

        # elif move=='leaderboard':

        else:
            await ctx.send('Please choose rock, paper, or scissors!')

    @commands.command(aliases=['8ball', 'eightball'])
    async def _8ball(self, ctx, *, question):
        response = ['As I see it, yes.',
                    'Ask again later.',
                    'Better not tell you now.',
                    'Cannot predict now.',
                    'Concentrate and ask again.',
                    'Don’t count on it.',
                    'It is certain.',
                    'It is decidedly so.',
                    'Most likely.',
                    'My reply is no.',
                    'My sources say no.',
                    'Outlook not so good.',
                    'Outlook good.',
                    'Reply hazy, try again.',
                    'Signs point to yes.',
                    'Very doubtful.',
                    'Without a doubt.',
                    'Yes.',
                    'Yes – definitely.',
                    'You may rely on it.']
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(response)}')


def setup(client):
    client.add_cog(Fun(client))
