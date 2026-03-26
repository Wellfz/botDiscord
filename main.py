import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("TOKEN")

permission = discord.Intents.all()
permission.message_content = True
permission.members = True
bot = commands.Bot("!",intents=permission)

@bot.command()
async def ola(ctx:commands.Context):
    user = ctx.author.display_name

    await ctx.reply(f'Olá, {user}!')





bot.run(token)