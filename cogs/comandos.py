import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
import os
from db import _Sessao, Usuario


class Comandos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command()
    async def leaderboard(self, interaction:discord.Interaction):
        with _Sessao() as sessao:
            topList = sessao.query(Usuario).order_by(Usuario.tempoEstudo.desc()).limit(10).all()
        embed = discord.Embed(title="LeaderBoard", color=discord.Colour.blue()) 
        description = ""
        for x, usuario in enumerate(topList):
            membro = interaction.guild.get_member(usuario.discord_id)
            if not membro:
                membroName = "Usuario desconhecido"
            else:
                membroName = membro.display_name
            tempoEmMinutos = usuario.tempoEstudo * 60
            horas, minutos = divmod(tempoEmMinutos, 60)
            description += f'{x+1} - {membroName} - {int(horas)}h {int(minutos)}min\n'

        embed.description = description
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Comandos(bot))