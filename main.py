import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
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

@bot.event
async def on_voice_state_update(member:discord.Member, before, after):
    user = member.display_name
    hora = datetime.now().strftime('%H:%M:%S')
    data = datetime.now().strftime('%d/%m/%Y')

    after = after.channel
    before = before.channel

    if(before is None and after is not None):
        print(f'{user} entrou no canal [{after}] as {hora} {data}')
    elif(before is not None and after is None):
        print(f'{user} saiu do canal [{before}] as {hora} {data}')
    elif(before is not None and after is not None):
        print(f'{user} saiu do canal [{before}] para o canal [{after}] as {hora} {data}')



bot.run(token)