import discord
from discord.ext import commands,tasks
from dotenv import load_dotenv
from datetime import datetime
from os import getenv
from os import listdir
from db import _Sessao, Usuario
from db import obterUsuario,contarLevel,contarXp
from time import sleep

load_dotenv()
token = getenv("TOKEN")

permission = discord.Intents.all()
permission.message_content = True
permission.members = True
bot = commands.Bot("!",intents=permission)
cargos = []

@bot.event
async def on_ready():
    resetarLeaderboard.start()
    global cargos
    guild = bot.guilds[0]
    cargos = [
        (0,  guild.get_role(1488422333151580211)),
        (3,  guild.get_role(1488590673614602349)),
        (7,  guild.get_role(1489782324898824232)),
        (12, guild.get_role(1489782378015490069)),
        (18, guild.get_role(1489782427047166053)),
        (25, guild.get_role(1489782458584142035)),
        (33, guild.get_role(1489782477815021619)),
        (42, guild.get_role(1489782500623388682)),
        (52, guild.get_role(1489782523222429786)),
        (63, guild.get_role(1489782544386756708)),
        (75, guild.get_role(1489782575370080257)),
    ]
    await carregarCogs()
    sync = await bot.tree.sync()
    print(f'{len(sync)} comandos sincronizados...')
    sleep(3.0)
    print(f"{bot.user.name} online!")

async def carregarCogs():
     for x in listdir('cogs'):
        if x.endswith('.py'):
            await bot.load_extension(f'cogs.{x[:-3]}')

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
        contarXp(member=member)
        contarLevel(member=member)
        await nivelCargo(member=member)

    elif(before is not None and after is not None and before != after and channel):
        print(f'{user} saiu do canal [{before}] as {datetime.now().strftime("%H:%M:%S")} para o canal [{after}] as {horaEntrada[member.id].strftime("%H:%M:%S")} {data}')
        registrarSaida(member=member)
        horaEntrada[member.id] = datetime.now()
        contarXp(member=member)
        contarLevel(member=member)
        await nivelCargo(member=member)

async def nivelCargo(member:discord.Member):
    if(member.id == bot.user):
         return

    with _Sessao() as sessao:
        user = obterUsuario(sessao=sessao,discord_id=member.id)

        for nivel_minimo, x in cargos:
            if user.level >= nivel_minimo:
                await member.add_roles(x)
        sessao.commit()

@tasks.loop(hours=170)
async def resetarLeaderboard():
    with _Sessao() as sessao:
        usuario_db = sessao.query(Usuario).all()
    for i in usuario_db:
        i.tempoEstudo = 0
        sessao.commit()
     
bot.run(token)