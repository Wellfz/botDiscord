import discord
from discord.ext import commands
from discord import app_commands
from db import obterUsuario,create_progress_bar
from db import _Sessao, Usuario

cargos_xp = [
    (0,      "Novato👦🏻"),
    (240,    "Aprendiz🧙🏻"),
    (720,    "Estudante📚"),
    (1800,   "Focado🔎"),
    (3600,   "Pesquisador📈"),
    (6000,   "Analista🧐"),
    (9600,   "Especialista🫔"),
    (13200,  "Mestre👨‍🔬"),
    (16800,  "Sábio😏"),
    (20400,  "Iluminado✨"),
    (24000,  "Lenda Acadêmica🐉"),
]

class Comandos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command()
    async def ranks(self, interaction:discord.Interaction):
        embed = discord.Embed(title="Ranks", color=0xEF9F27)
        botPhoto = interaction.client.user.display_avatar.url     
        
        description = ""
        for cargo in cargos_xp:
            description+=(f"{cargo[1]}  -  {cargo[0]}XP\n")

        embed.description = description
        embed.set_thumbnail(url=botPhoto)
        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def leaderboard(self, interaction:discord.Interaction):
        botName = self.bot.user.name
        
        with _Sessao() as sessao:
            topList = sessao.query(Usuario).order_by(Usuario.tempoEstudo.desc()).limit(10).all()
        embed = discord.Embed(title="LeaderBoard", color=0xEF9F27) 
        description = ""
        for x, usuario in enumerate(topList):
            membro = interaction.guild.get_member(usuario.discord_id)
            if not membro:
                membroName = interaction.user.display_name
            else:
                membroName = membro.display_name
            tempoEmMinutos = usuario.tempoEstudo * 60
            horas, minutos = divmod(tempoEmMinutos, 60)
            description += f'{x+1} - {membroName} - {int(horas)}h {int(minutos)}min\n'

        embed.set_footer(text=f"{botName}")
        embed.description = description
        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def perfil(self, interaction:discord.Interaction):
        botName = self.bot.user.name
        memberUser = interaction.user.display_name
        corCargoUser = interaction.user.roles[-1].color
        
        with _Sessao() as sessao:
            usuario_db = obterUsuario(sessao=sessao,discord_id=interaction.user.id)
            level = usuario_db.level
            xp = usuario_db.xp
            topList = sessao.query(Usuario).order_by(Usuario.tempoEstudo.desc()).limit(10).all()

            tempoEmMinutos = usuario_db.tempoEstudo * 60
            horas, minutos = divmod(tempoEmMinutos, 60)

        embed = discord.Embed(title=f"Perfil de {memberUser}", color=corCargoUser)
        embed.description = f"Membro desde {interaction.user.joined_at.strftime('%d/%m/%Y')}"
        embed.set_footer(text=f"{botName}")
        embed.set_thumbnail(url=interaction.user.avatar)

        ranking = "+10"

        for i, posicao in enumerate(topList):
            if posicao.discord_id == interaction.user.id:
                ranking = str(i+1)
                break

        embed.add_field(name="Nivel⚡", value=level,inline=True)
        embed.add_field(name="XP TOTAL🧪", value=f"{int(xp)} XP",inline=True)
        embed.add_field(name="RANKING",value=f"#{ranking}",inline=True)

        embed.add_field(name="HORAS TOTAIS", value=f"{int(horas)}h {int(minutos)}min")

        for i, cargo in enumerate(cargos_xp):
            if usuario_db.xp >= cargo[0] and usuario_db.xp < cargos_xp[i+1][0]:
                cargoAtualName = cargo[1]
                break

        embed.add_field(name="CARGO ATUAL", value=cargoAtualName)
        embed.add_field(name="",value="\u200b",inline=True)

        for i, cargo in enumerate(cargos_xp):
            if usuario_db.xp >= cargo[0] and usuario_db.xp < cargos_xp[i+1][0]:
                xpCargoAtual = cargo[0]
                xpCargoProximo = cargos_xp[i+1][0]
                break

        percentage = (usuario_db.xp - xpCargoAtual) / (xpCargoProximo - usuario_db.xp)

        cargoProximoName = cargos_xp[i+1][1]

        embed.add_field(name=f"Progresso -> {cargoProximoName}",value=create_progress_bar(percentage=percentage))

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Comandos(bot))