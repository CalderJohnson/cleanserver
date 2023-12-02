"""Message templates for Discord bot"""
import discord
from database import Database

async def error(ctx, content):
    """Display an error message"""
    message = discord.Embed(title="Error", color=0xFF0000, description=content)
    await ctx.send(embed=message)

async def success(ctx, content):
    """Display a success message"""
    message = discord.Embed(title="Success", color=0x00FF00, description=content)
    await ctx.send(embed=message)

async def info(ctx, content):
    """Misc message"""
    message = discord.Embed(title="Info", color=0x00FFA2, description=content)
    await ctx.send(embed=message)

async def log(message, score):
    """Log a message to the server's log channel"""
    if Database.get_server(message.guild.id) is None:
        Database.add_server(message.guild.id)
    server = Database.get_server(message.guild.id)
    if server["channel"] == 0:
        error(message.channel.send, "No channel set. Please set a channel using `/channel <#channel>`")
        return
    channel = message.guild.get_channel(server["channel"])
    user = message.author
    message = discord.Embed(title="Log", color=0x00FFA2, description=f"Message logged with score {score} from user <@{user.id}>: {message.content}")
    await channel.send(embed=message)
