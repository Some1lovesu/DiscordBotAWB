import discord
from discord.ext import commands
import logging

# Setup basic logging for debugging
logging.basicConfig(level=logging.INFO)

# Define all intents for the bot
intents = discord.Intents.all()

# Initialize the bot with a command prefix and all intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    # Logs a message to the console when the bot logs in successfully
    logging.info(f'Logged in as {bot.user.name}')

@bot.command(name='sc')
async def setup_server(ctx):
    # Ensures the command issuer has permission to manage channels
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("You don't have permission to manage channels!")
        return

    guild = ctx.guild  # Represents the server where the command is issued

    # Ensure the channel names match exactly what's on your server
    general_channel_name = "general"  # Update this to match the exact name
    general_voice_channel_name = "General"  # Update this to match the exact name

    try:
        # Delete "General" text channel if it exists
        general_text_channel = discord.utils.get(guild.channels, name=general_channel_name,
                                                 type=discord.ChannelType.text)
        if general_text_channel:
            await general_text_channel.delete()
            logging.info('Deleted the "General" text channel')

        # Delete "General Voice Channel" if it exists
        general_voice_channel = discord.utils.get(guild.channels, name=general_voice_channel_name,
                                                  type=discord.ChannelType.voice)
        if general_voice_channel:
            await general_voice_channel.delete()
            logging.info('Deleted the "General Voice Channel"')

    except Exception as e:
        logging.error(f'An error occurred during channel deletion: {e}')
        await ctx.send('An error occurred during the channel deletion. Please check the logs for more details.')

    # After handling potential deletions, proceed with the setup
    try:
        # Create the member count channel and other setup actions
        member_count_channel_name = f'Members: {guild.member_count}'
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            guild.me: discord.PermissionOverwrite(view_channel=True)
        }
        if guild.owner:
            overwrites[guild.owner] = discord.PermissionOverwrite(view_channel=True)

        await guild.create_voice_channel(name=member_count_channel_name, overwrites=overwrites, position=0)
        logging.info(f'Created member count channel: {member_count_channel_name}')
    except Exception as e:
        logging.error(f'An error occurred during member count channel setup: {e}')
        await ctx.send('An error occurred during the member count channel setup. Please check the logs for more details.')

    # Names for the existing categories under which channels will be organized
    text_category_name = 'Text Channels'  # Name of the existing category for text channels
    voice_category_name = 'Voice Channels'  # Name of the existing category for voice channels

    # Try to find existing categories by name
    text_category = discord.utils.get(guild.categories, name=text_category_name)
    voice_category = discord.utils.get(guild.categories, name=voice_category_name)

    if not text_category:
        logging.warning(f'Category "{text_category_name}" not found. Consider creating it manually.')
    if not voice_category:
        logging.warning(f'Category "{voice_category_name}" not found. Consider creating it manually.')

    # Channel names to be created
    text_channel_names = ['General Chat', 'Meme Chat', 'Off-topic Chat']
    voice_channel_names = ['General VC', 'Regulation VC', 'Standard VC']
    welcome_channel_name = 'Welcome'  # This should be unique to avoid conflicts with the original channel

    # Create text channels under the found text category, if it exists
    for name in text_channel_names:
        if text_category:
            await guild.create_text_channel(name, category=text_category)
            logging.info(f'Created text channel: {name} under {text_category_name}')
        else:
            logging.info(
                f'Skipped creating text channel: {name} because category "{text_category_name}" does not exist.')

    # Create voice channels under the found voice category, if it exists
    for name in voice_channel_names:
        if voice_category:
            await guild.create_voice_channel(name, category=voice_category)
            logging.info(f'Created voice channel: {name} under {voice_category_name}')
        else:
            logging.info(
                f'Skipped creating voice channel: {name} because category "{voice_category_name}" does not exist.')

    # Additional code for welcome channel and other setup actions...
    # Additional code for welcome channel and other setup actions...

    welcome_channel = await guild.create_text_channel(welcome_channel_name)
    welcome_message = await welcome_channel.send('Welcome to the server! Please choose reactions below to show what content you are interested in doing.')

    reactions = ['👋', '😄', '🎉', '✅', '📚']
    for emoji in reactions:
        await welcome_message.add_reaction(emoji)

    other_bot_client_id = '1206607367551328307'
    permissions_integer = '8'
    invite_link = f'https://discord.com/oauth2/authorize?client_id={1206607367551328307}&permissions={8}&scope=bot'
    await ctx.send(f'Invite the other bot using this link: {invite_link}')

    await welcome_channel.send("Server Setup Complete: Please Begin Degenerate Behavior")
    await ctx.send('Server setup is complete.')


# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run('')
