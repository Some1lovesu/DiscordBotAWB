import discord
from discord.ext import commands
import youtube_dl

# Define intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.voice_states = True  # This is required to receive events for voice state changes

# Set up the bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

# Define youtube_dl options
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.command()
async def join(ctx):
    """Joins the voice channel of the message author."""
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        try:
            await channel.connect()
        except discord.ClientException as e:
            await ctx.send("I'm already connected to a voice channel.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
    else:
        await ctx.send("You are not in a voice channel. Please join a voice channel first.")



@bot.command()
async def leave(ctx):
    """Leaves the voice channel"""
    await ctx.voice_client.disconnect()


@bot.command()
async def play(ctx, url):
    """Plays audio from a YouTube URL"""
    if not ctx.voice_client:
        await ctx.invoke(join)

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ctx.voice_client.stop()
    ctx.voice_client.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                          after=lambda e: print('Player error: %s' % e) if e else None)


@bot.command()
async def pause(ctx):
    """Pauses the current playing audio"""
    ctx.voice_client.pause()


@bot.command()
async def resume(ctx):
    """Resumes the audio"""
    ctx.voice_client.resume()


@bot.command()
async def stop(ctx):
    """Stops the audio"""
    ctx.voice_client.stop()


# Replace 'YOUR_BOT_TOKEN_HERE' with your bot's token
bot.run('MTIwNzE4NTEzMjY1NDY5MDM2NQ.GSeeXl.15CxoNKS1NKycRAqMYyzxmerZMhfPnjj5Cmyx4')
