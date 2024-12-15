from datetime import date
from typing import List
from sqlmodel import SQLModel, Field, Relationship


class Room(SQLModel, table=True):
    __tablename__ = "room"

    number: int = Field(primary_key=True)
    floor: int = Field(ge=2, le=5)


class DutyDay(SQLModel, table=True):
    __tablename__ = "duty_day"

    id: int | None = Field(default=None, primary_key=True)
    duty_date: date = Field(nullable=False, unique=True)
    floor: int = Field(ge=2, le=5, nullable=False)
    is_done: bool = Field(default=False, description="Статус дежурства")
    photo_url: str | None = Field(default=None, description="Ссылка на фото отчёта")
    report_room_number: int | None = Field(
        default=None, description="Комната, отправившая отчёт"
    )

    rooms: List["DutyRoom"] = Relationship(back_populates="duty_day")


class DutyRoom(SQLModel, table=True):
    __tablename__ = "duty_room"

    duty_day_id: int = Field(
        foreign_key="duty_day.id", primary_key=True, ondelete="CASCADE"
    )
    room_number: int = Field(
        foreign_key="room.number",
        primary_key=True,
    )
    duty_day: DutyDay = Relationship(back_populates="rooms")
    room: Room = Relationship()
