import os

from sqlalchemy import create_engine, DateTime, func, BigInteger, select,delete
from sqlalchemy.orm import DeclarativeBase, declared_attr, Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from dotenv import load_dotenv
load_dotenv()

import psycopg2

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
session = Session(bind=engine)


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower() + 's'


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return (f'User(id {self.id!r},full_name {self.full_name!r}, last_name {self.last_name!r}, '
                f' user_id {self.user_id!r},created_at {self.created_at!r}, username {self.username!r})')
class Kino(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    file_id: Mapped[str] = mapped_column(nullable=True)
    message_id: Mapped[int] = mapped_column(nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return f'Kino (id{self.id!r}, file_id{self.file_id!r}, message_id{self.message_id!r},created_at{self.created_at!r})'
class Kanal(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    kanal_url: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    def __repr__(self) -> str:
        return f'Kanal(id{self.id!r}, kino_url {self.kanal_url!r},created_at{self.created_at!r})'


Base.metadata.create_all(engine)



