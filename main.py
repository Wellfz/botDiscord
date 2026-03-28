import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
import os
from db import _Sessao, Usuario

load_dotenv()
token = os.getenv("TOKEN")

permission = discord.Intents.all()
permission.message_content = True
permission.members = True
bot = commands.Bot("!",intents=permission)

def obterUsuario(sessao, discord_id):
        usuario_db = sessao.query(Usuario).filter_by(discord_id=discord_id).first()
        if not usuario_db:
            usuario_db = Usuario(discord_id=discord_id)
            sessao.add(usuario_db)
            sessao.commit()
        return usuario_db

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
        horasEstudadas = datetime.now() - horaEntrada[member.id]

        horasEstudadasFormat = horasEstudadas.seconds / 3600

        with _Sessao() as sessao:
            usuario_db = obterUsuario(sessao, member.id)
            usuario_db.tempoEstudo += horasEstudadasFormat
            sessao.commit()
            
    elif(before is not None and after is not None and channel):
        print(f'{user} saiu do canal [{before}] as {datetime.now()} para o canal [{after}] as {horaEntrada[member.id].strftime("%H:%M:%S")} {data}')
        horasEstudadas = datetime.now() - horaEntrada[member.id]

        horasEstudadasFormat = horasEstudadas.seconds / 3600

        with _Sessao() as sessao:
            usuario_db = obterUsuario(sessao, member.id)
            usuario_db.tempoEstudo += horasEstudadasFormat
            sessao.commit()



bot.run(token)