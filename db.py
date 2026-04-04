import discord
from sqlalchemy import create_engine, Column, String, Integer,DateTime, BigInteger, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
from os import getenv
from math import floor,sqrt


load_dotenv()
DBTOKEN = getenv("DBTOKEN")

engine = create_engine(DBTOKEN,
                       pool_pre_ping=True,
                       pool_recycle=1800,
                       pool_size=10,
                       max_overflow=20,
                       pool_timeout=30
)
Base = declarative_base()
_Sessao = sessionmaker(engine)

def create_progress_bar(percentage, length=15):
    filled_len = int(length * percentage)
    bar = '🟩' * filled_len + '⬛' * (length - filled_len)
    return bar


def obterUsuario(sessao, discord_id):
    usuario_db = sessao.query(Usuario).filter_by(discord_id=discord_id).first()
    if not usuario_db:
        usuario_db = Usuario(discord_id=discord_id)
        sessao.add(usuario_db)
        sessao.commit()
    return usuario_db

def contarLevel(member:discord.Member):
    with _Sessao() as sessao:
        usuario_db = obterUsuario(sessao=sessao,discord_id=member.id)
        N = usuario_db.xp
        level = floor((-1 + sqrt(1 + 2*N/3)) / 2)

        usuario_db.level = level
        sessao.commit()

def contarXp(member:discord.Member):
    with _Sessao() as sessao:
        usuario_db = obterUsuario(sessao=sessao,discord_id=member.id)
        xpGanho = (usuario_db.tempoEstudo) * 12 - usuario_db.xp
        if xpGanho > 0:
            usuario_db.xp += xpGanho
        sessao.commit()

class Usuario(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    discord_id = Column(BigInteger, unique=True)
    tempoEstudo = Column(Float, default=0)
    xp = Column(Float, default=0)
    level = Column(Integer, default=0)

Base.metadata.create_all(engine)