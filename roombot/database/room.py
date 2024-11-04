import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

from roombot.config import engine
from roombot.config import session

Base = declarative_base()


class Room(Base):
    __tablename__ = "rooms"
    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
    )
    owner = sqlalchemy.Column(
        sqlalchemy.String,
        unique=True,
        nullable=False,
    )
    number = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable=False,
    )
    contact = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
    )
    full_name_owner = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
    )


class BannedUser(Base):
    __tablename__ = "bannedusers"
    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
    )
    owner = sqlalchemy.Column(
        sqlalchemy.String,
        unique=True,
        nullable=False,
    )


Base.metadata.create_all(engine)


def get_or_create_room(owner_id: int) -> Room:
    room = session.query(Room).filter(Room.owner == owner_id).first()
    if room:
        return room

    room = Room(
        owner=owner_id,
    )
    return room


def get_room_by_owner(owner_id: int) -> Room | None:
    return session.query(Room).filter(Room.owner == owner_id).first()


def get_room_by_number(number: int) -> list[Room] | None:
    return session.query(Room).filter(Room.number == number).all()


def delete_room_by(room: Room) -> None:
    session.delete(room)
    session.commit()
