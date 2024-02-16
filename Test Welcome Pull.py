import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True  # Enable intents for tracking members joining

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        await guild.system_channel.send(f'Welcome {member.mention} to {guild.name}! 🎉')
def main() -> None:
bot.run('MTIwNjYwNzM2NzU1MTMyODMwNw.GaxnkO.UdJ7WMTAgJFN3zQUhDZgRM5TL3xeFcJWNkSGa8')

