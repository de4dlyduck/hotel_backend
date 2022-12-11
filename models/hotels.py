from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Date, Boolean
from models.database import base
from dataclasses import dataclass


@dataclass
class Reviews(base):
    id: int
    description: str
    rating: int
    id_rooms: int
    id_profile: int

    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=True)
    rating = Column(Integer, nullable=True)
    id_rooms = Column(Integer, ForeignKey("rooms.id"))
    id_profile = Column(Integer, ForeignKey("profiles.id"))


@dataclass
class Rooms(base):
    id: int
    description: str
    cost: float
    personScore: int
    vans: int
    bedScore: int
    occupied: bool
    photo: str

    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=True)
    cost = Column(Float, nullable=True)
    personScore = Column(Integer, nullable=True)
    vans = Column(Integer, nullable=True)
    bedScore = Column(Integer, nullable=True)
    occupied = Column(Boolean)
    photo = Column(Text)


@dataclass
class Profile(base):
    id: int
    name: str
    surname: str
    patronymic: str
    password: str
    serial: str
    nomber: str
    mail: str
    telNumber: str
    type: str

    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    surname = Column(String(25))
    patronymic = Column(String(25))
    password = Column(Text, nullable=True)
    serial = Column(Text)
    nomber = Column(Text)
    mail = Column(String(25), unique=True, nullable=True)
    telNumber = Column(Text, unique=True, nullable=True)
    type = Column(Text, nullable=True)


@dataclass
class Penalties(base):
    id: int
    description: str
    cost: float
    id_user: int

    __tablename__ = 'penalties'
    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=True)
    cost = Column(Float, nullable=True)
    id_user = Column(Integer, ForeignKey("profiles.id"), nullable=True)


@dataclass
class Date(base):
    id: int
    id_user: int
    id_room: int
    first_day: str
    last_day: str
    code: str
    __tablename__ = 'dates'
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('profiles.id'), nullable=True)
    id_room = Column(Integer, ForeignKey("rooms.id"), nullable=True)
    first_day = Column(String, nullable=True, unique=True)
    last_day = Column(String, nullable=True, unique=True)
    code = Column(Text,nullable=True, unique=True)
