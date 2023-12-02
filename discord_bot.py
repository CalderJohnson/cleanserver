"""Discord frontend for Cleanserver"""
import os
import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv

from model.interface import ModelInterface
from messages import info, error, success, log
from database import Database

# Setup

prefix = 'c!'
intents = discord.Intents.default()
intents.message_content = True
bot = Bot(command_prefix=prefix, intents=intents, help_command=None)
bot.remove_command('help')

Database.start_db()
interface = ModelInterface()
load_dotenv()

# Events

@bot.event
async def on_ready():
    """Triggers when the bot is running"""
    activity = discord.Game(name="Keeping your server clean!", type=2)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("Discord bot online")

@bot.event
async def on_message(message):
    """Event handler for messages"""
    if message.author == bot.user:
        return
    else:
        print(message.content)
        score = interface.analyze_message(message.content)
        print(score)
        mode = Database.get_server(message.guild.id)["mode"]
        print(mode)
        if mode == 0 and score < -2:
            await log(message, score)
        elif mode == 1 and score < -3.5:
            await log(message, score)
        elif mode == 2 and score < -5:
            await log(message, score)

# Commands

@bot.slash_command(name="help", description="Help command")
async def help(ctx):
    """Displays a help message"""
    message = discord.Embed(title="Info", color=0x00FFA2, description="""
        **Cleanserver is an AI powered discord moderation bot. It uses machine learning to detect toxic messages and automatically flag them in a channel of your choice.**
                            
        **/help** - Displays this message
        **/channel <#channel-id>** - Sets the channel for the bot to log moderation info to
        **/mode <mode>** - Sets the mode for the bot to use. Modes are: `strict`, `medium`, `lenient`
        """)
    await info(ctx, message)

@bot.slash_command(name="set_channel", description="Set the channel for the bot to log moderation info to")
async def set_channel(ctx, channel: discord.channel.TextChannel):
    """Set the channel for the bot to log moderation info to"""
    if type(channel) is not discord.channel.TextChannel:
        await error(ctx, "Invalid channel. Please provide a valid channel")
        return
    if Database.get_server(ctx.guild.id) is None:
        Database.add_server(ctx.guild.id)
    Database.update_channel(ctx.guild.id, channel.id)
    await success(ctx, f"Successfully updated channel to <#{channel.id}>")

@bot.slash_command(name="set_mode", description="Set the level of moderation for the bot")
async def set_mode(ctx, mode: str):
    """Change the level of moderation for the bot"""
    if mode == "strict":
        mode = 0
    elif mode == "medium":
        mode = 1
    elif mode == "lenient":
        mode = 2
    else:
        await error(ctx, "Invalid mode. Valid modes are: `strict`, `medium`, `lenient`")
        return
    if Database.get_server(ctx.guild.id) is None:
        Database.add_server(ctx.guild.id)
    Database.update_mode(ctx.guild.id, mode)
    await success(ctx, f"Successfully updated mode to {mode}")

bot.run(os.getenv("DISCORD_TOKEN"))
