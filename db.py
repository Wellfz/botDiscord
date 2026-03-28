from sqlalchemy import create_engine, Column, String, Integer,DateTime, BigInteger, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DBTOKEN = os.getenv("DBTOKEN")

engine = create_engine(DBTOKEN)
Base = declarative_base()
_Sessao = sessionmaker(engine)

class Usuario(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    discord_id = Column(BigInteger, unique=True)
    tempoEstudo = Column(Float, default=0)

Base.metadata.create_all(engine)