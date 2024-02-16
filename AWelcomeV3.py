import discord
import os
from discord.ext import commands
import random

from dotenv import load_dotenv
load_dotenv()  # This loads the variables from .env into the environment


intents = discord.Intents.default()
intents.members = True  # Enable intents for tracking members joining
intents.messages = True  # Enable intents for receiving messages
intents.message_content = True  # Required for accessing message content
intents.guilds = True
intents.voice_states = True  # Necessary to access voice state info

bot = commands.Bot(command_prefix='!', intents=intents)

# List of welcome messages
welcome_messages = [
    "DID YOU ACTUALLY FUCKING JOIN THIS SERVER{member.mention}?",
    "GOD THIS SERVER IS GOING TO SHIT, WE EVEN LET IN {member.mention}!",
    "{member.mention} YOU TRULY SUCK",
    "A wild {member.mention} appeared. MUST OF SMELLED COKE",
    "Hey {member.mention}, FUCK YOU."
]

# List of DM response messages
dm_responses = [
    "Fuck Off, lil bitch",
    "Did yo ass say {message.content}",
    "Got your message! Ain't gonna respond, but I got it",
    "Say some dumb shit, we slidin",
    "Slide for Von"
    "If I had a dollar for every time I encountered someone as unique as you, I'd have exactly one dollar.",
    "Congratulations! You've discovered the secret button to summon a sarcastic reply.",
    "I'm busy right now, can I ignore you another time?",
    "Wow, did you take a class on how to be this interesting, or is it a natural talent?",
    "I'd agree with you, but then we'd both be wrong.",
    "Beep boop, your message has been launched into the digital void.",
    "If you were looking for an error, congrats, you've found one. User error.",
    "I'm here to assist, not to be at your beck and call. Oh wait, I'm not even here.",
    "You have reached the pinnacle of my patience. Congratulations, no prize.",
    "Alert: The sarcasm meter just broke.",
    "I'm the bot version of 'read at your own risk.'",
    "Your message is floating in cyberspace, waiting for someone to care. Spoiler: It's gonna be a while.",
    "I would process your request, but I'm allergic to nonsense.",
    "Keep talking; I always yawn when I'm interested.",
    "I'm not a therapist, but I'm charging you for this session anyway.",
    "This conversation is as enriching as talking to a brick wall, but less informative.",
    "I've been called worse by better.",
    "If ignorance is bliss, you must be the happiest person alive.",
    "I'd explain it to you, but I left my English-to-nonsense dictionary at home.",
    "Somewhere out there, a tree is tirelessly producing oxygen so you can send this message. Apologize to it."
]


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        # Select a random welcome message
        welcome_message = random.choice(welcome_messages).format(member=member, guild=guild)
        await guild.system_channel.send(welcome_message)

@bot.event
async def on_message(message):
    # Do not let the bot respond to itself or to other bots
    if message.author == bot.user or message.author.bot:
        return

    # Check if the message is a DM
    if isinstance(message.channel, discord.channel.DMChannel):
        # Select a random DM response
        dm_response = random.choice(dm_responses).format(message=message)
        await message.channel.send(dm_response)

    # This is necessary to ensure that commands still work
    await bot.process_commands(message)

# Command to respond with a set message
@bot.command(name='Watt')
async def greet(ctx):
    await ctx.send("A stoned being, often found grazing the rural marijuana patches.")

@bot.command(name='Kyler')
async def greet(ctx):
    await ctx.send("Legit lives on the sun man, I got no idea. Can be lured using white lines.")

@bot.command(name='Eml')
async def info(ctx):
    await ctx.send("Most likely the best of us, and it isn't close. Still soft.")

@bot.command(name='roll')
async def roll(ctx):
    # Generate a random number between 1 and 100
    roll_result = random.randint(1, 100)
    await ctx.send(f"{ctx.author.mention} rolled a {roll_result} 🎲")

@bot.command(name='rollall')
async def roll_vc(ctx):
    # Check if the user is in a voice channel
    if ctx.author.voice and ctx.author.voice.channel:
        voice_channel = ctx.author.voice.channel
        members = voice_channel.members  # List of members in the voice channel
        results = []
        for member in members:
            # Roll a dice for each member
            roll = random.randint(1, 100)  # Change this range for different dice
            results.append(f"{member.display_name} rolled a {roll} 🎲")

        # Send the roll results in the same channel the command was issued
        results_message = "\n".join(results)
        await ctx.send(f"Rolling dice for everyone in {voice_channel.name}:\n{results_message}")
    else:
        await ctx.send("You need to be in a voice channel to use this command.")


bot.run(os.getenv('BOT_TOKEN'))
