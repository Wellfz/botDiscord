import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
from os import getenv
import os
from db import _Sessao, Usuario

load_dotenv()
token = getenv("TOKEN")

permission = discord.Intents.all()
permission.message_content = True
permission.members = True
bot = commands.Bot("!",intents=permission)

@bot.event
async def on_ready():
    await carregarCogs()
    await bot.tree.sync()

async def carregarCogs():
     for x in os.listdir('cogs'):
        if x.endswith('.py'):
            await bot.load_extension(f'cogs.{x[:-3]}')

def obterUsuario(sessao, discord_id):
        usuario_db = sessao.query(Usuario).filter_by(discord_id=discord_id).first()
        if not usuario_db:
            usuario_db = Usuario(discord_id=discord_id)
            sessao.add(usuario_db)
            sessao.commit()
        return usuario_db

def registrarSaida(member:discord.Member):
        horasEstudadas = datetime.now() - horaEntrada[member.id]

        horasEstudadasFormat = horasEstudadas.total_seconds() / 3600

        with _Sessao() as sessao:
            usuario_db = obterUsuario(sessao, member.id)
            usuario_db.tempoEstudo = round(usuario_db.tempoEstudo + horasEstudadasFormat, 2)    
            sessao.commit()

horaEntrada = {}
@bot.event
async def on_voice_state_update(member:discord.Member, before, after):
    channel = member.guild.get_channel(1481490068706300005)
    user = member.display_name

    data = datetime.now().strftime('%d/%m/%Y')
    after = after.channel
    before = before.channel

    if(before is None and after is not None and channel):
        horaEntrada[member.id] = datetime.now()
        print(f'{user} entrou no canal [{after}] as {horaEntrada[member.id].strftime("%H:%M:%S")} {data}')

    elif(before is not None and after is None and channel):
        print(f'{user} saiu do canal [{before}] as {datetime.now().strftime("%H:%M:%S")} {data}')
        registrarSaida(member=member)

    elif(before is not None and after is not None and channel):
        print(f'{user} saiu do canal [{before}] as {datetime.now().strftime("%H:%M:%S")} para o canal [{after}] as {horaEntrada[member.id].strftime("%H:%M:%S")} {data}')
        registrarSaida(member=member)
        horaEntrada[member.id] = datetime.now()

bot.run(token)