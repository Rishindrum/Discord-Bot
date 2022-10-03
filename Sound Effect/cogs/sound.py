import discord
import youtube_dl
import os
import shutil
from discord.utils import get
import urllib.parse, urllib.request, re
from os import system
from discord.ext import commands
from arghandler import ArgumentHandler


async def youtube(search):
    query_string = urllib.parse.urlencode({
        'search_query': search
    })
    htm_content = urllib.request.urlopen(
        'https://www.youtube.com/results?' + query_string
    )
    search_results = re.findall('href=\"\\/watch\\?v=(.{11})', htm_content.read().decode())
    print(search_results)
    x = 1
    embed = discord.Embed(
        color=discord.Colour.blue()
    )
    while (x - 1) * 2 < len(search_results) and x < 6:
        embed.add_field(name=str(x) + ".", value=f'https://www.youtube.com/watch?v={search_results[(x - 1) * 2]}\n',
                        inline=True)
        x += 1

    return embed


async def link(num, search):
    query_string = urllib.parse.urlencode({
        'search_query': search
    })
    htm_content = urllib.request.urlopen(
        'https://www.youtube.com/results?' + query_string
    )
    search_results = re.findall('href=\"\\/watch\\?v=(.{11})', htm_content.read().decode())
    print(search_results)
    return 'https://www.youtube.com/watch?v=' + search_results[2 * (num - 1)]  # 0 gives one result

class Sound(commands.Cog):
    def __init__(self, client):
        self.client = client

    global queues
    queues = {}
    @commands.command()
    async def join(self, ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            print(f'Joined {channel}')
        await ctx.send(f'Joined {channel}')

    @commands.command()
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            print(f'Left {channel}')
            await ctx.send(f'Left {channel}')
        else:
            print('I am not in a voice channel')
            await ctx.send('I am not in a voice channel')

    @commands.command()
    async def test(self, ctx):
        search='Hello'
        query_string = urllib.parse.urlencode({
            'query': search
        })
        print(query_string)
        htm_content = urllib.request.urlopen(
            'https://www.youtube.com/results?' + query_string
        )
        print(htm_content)
        search_results = re.findall('href=\"\\/watch\\?v=(.{11})', htm_content.read().decode())
        print(search_results)
        await ctx.send(embed=await youtube('hello'))
        #await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])

    @commands.command(aliases=['p', 'pla', 'Play', 'P'])
    async def play(self, ctx, *, url):
        def check_queue():
            Queue_infile = os.path.isdir("./Queue")
            if Queue_infile is True:
                DIR = os.path.abspath(os.path.realpath("Queue"))
                length = len(os.listdir(DIR))
                still_q = length - 1
                try:
                    first_file = os.listdir(DIR)[0]
                except:
                    print("No more queued song(s)\n")
                    queues.clear()
                    return
                main_location = os.path.dirname(os.path.realpath(__file__))
                if '\\cogs' in main_location:
                    main_location = main_location[0:len(main_location)-5]
                song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
                if length != 0:
                    print("Song done, playing next queued\n")
                    print(f"Songs still in queue: {still_q}")
                    song_there = os.path.isfile("song.mp3")
                    if song_there:
                        os.remove("song.mp3")
                    shutil.move(song_path, main_location)
                    for file in os.listdir("./"):
                        if file.endswith(".mp3"):
                            os.rename(file, 'song.mp3')

                    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume = 0.13

                else:
                    queues.clear()
                    return

            else:
                queues.clear()
                print("No songs were queued before the ending of the last song\n")

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                queues.clear()
                print("Removed old song file")
        except PermissionError:
            print("Trying to delete song file, but it's being played")
            await ctx.send("ERROR: Music Playing")
            return

        Queue_infile = os.path.isdir("./Queue")
        try:
            Queue_folder = "./Queue"
            if Queue_infile is True:
                print("Removed old Queue folder")
                shutil.rmtree(Queue_folder)
        except:
            print("No old Queue folder")

        await ctx.send("Getting everything ready now")

        voice = get(self.client.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print("Downloading audio now\n")
                ydl.download([url])
        except:
            print("That\'s not a fricking youtube url, so we finna search it up")
            await ctx.send(embed=await youtube(str(url)))
            await ctx.send('Choose a number from 1-5, depending on what you want to play.')

            def check(m):
                return m.content == '1' or m.content == '2' or m.content == '3' or m.content == '4' or m.content == '5'

            msg = await self.client.wait_for('message', check=check)
            await ctx.send("Getting song ready now")
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print("Downloading audio now\n")
                ydl.download([await link(int(msg.content), url)])
            """print("That\'s not a fricking youtube url, so we finna use spotify")
            c_path = os.path.dirname(os.path.realpath(__file__))
            system("spotdl -f " + '"' + c_path + '"' + " -s " + url)"""

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f"Renamed File: {file}\n")
                os.rename(file, "song.mp3")

        voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.13
        try:
            nname = name.rsplit("-", 2)
            await ctx.send(f'Playing: {nname[0]}')
        except:
            await ctx.send('Playing song.')
        print("playing\n")

    @commands.command(aliases=['pa', 'pau', 'paus', 'Pa', 'Pau', 'Paus'])
    async def pause(self, ctx):

        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print('Music paused')
            voice.pause()
            await ctx.send('Music paused')
        else:
            print("Music not playing failed pause")
            await ctx.send("Music not playing failed pause")

    @commands.command(aliases=['r', 'res', 'R', 'Res', 'Resume'])
    async def resume(self, ctx):

        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            print('Resumed music')
            voice.resume()
            await ctx.send('Resumed music')
        else:
            print("Music is not paused")
            await ctx.send("Music is not paused")

    @commands.command(aliases=['s', 'ski', 'S', 'Ski', 'Skip'])
    async def skip(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        queues.clear()

        if voice and voice.is_playing():
            print("Music skipped")
            voice.stop()
            await ctx.send("Music skipped")
        else:
            print("No music playing failed to skip")
            await ctx.send("No music playing failed to skip")

    @commands.command(aliases=['st', 'sto', 'St', 'Sto', 'Stop'])
    async def stop(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        queues.clear()

        queue_infile = os.path.isdir("./Queue")
        if queue_infile is True:
            shutil.rmtree("./Queue")

        if voice and voice.is_playing():
            print("Music stopped")
            voice.stop()
            await ctx.send("Music stopped")
        else:
            print("No music playing failed to stop")
            await ctx.send("No music playing failed to stop")

    @commands.command(aliases=['q', 'que', 'Q', 'Que', 'Queue'])
    async def queue(self, ctx, *, url):
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is False:
            os.mkdir("Queue")
        DIR = os.path.abspath(os.path.realpath("Queue"))
        q_num = len(os.listdir(DIR))
        q_num += 1
        add_queue = True
        while add_queue:
            if q_num in queues:
                q_num += 1
            else:
                add_queue = False
                queues[q_num] = q_num

        queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': queue_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print('Downloading audio now \n')
                ydl.download([url])
        except:
            print("That\'s not a fricking youtube url, so we finna search it up")
            await ctx.send(embed=await youtube(url))
            await ctx.send('Choose a number from 1-5, depending on what you want to play.')

            def check(m):
                return m.content == '1' or m.content == '2' or m.content == '3' or m.content == '4' or m.content == '5'

            msg = await self.client.wait_for('message', check=check)
            await ctx.send("Getting song ready now")
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print("Downloading audio now\n")
                ydl.download([await link(int(msg.content), url)])
            # q_path = os.path.abspath(os.path.realpath("Queue"))
            # system(f"spotdl -ff song{q_num} -f " + '"' + q_path + '"' + " -s " + url)

        await ctx.send("Adding song " + str(q_num) + " to the queue")

        print('Song added to queue\n')

    
def setup(client):
    client.add_cog(Sound(client))
