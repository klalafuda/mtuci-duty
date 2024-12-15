from datetime import date
from sqlmodel import SQLModel, Field
from pydantic import conlist


class DutyDayCreate(SQLModel):
    duty_date: date = Field(default=..., description="Дата дежурства")
    floor: int = Field(default=..., ge=2, le=5, description="Этаж")
    rooms: conlist(int, min_length=1, max_length=2) = Field(
        default=..., description="От 1 до 2 номеров комнат"
    )


class DutyDayRead(SQLModel):
    duty_date: date
    floor: int
    is_done: bool
    photo_url: str | None
    rooms: list[int]
    report_room_number: int | None


class DutyDayReportUpdate(SQLModel):
    duty_date: date = Field(default=..., description="Дата дежурства")
    report_room_number: int = Field(
        default=..., description="Комната, отправляющая отчёт"
    )
    is_done: bool = Field(
        default=..., description="Статус дежурства (выполнено или нет)"
    )
    # Фото будет приниматься отдельно через FormData, не в модели.
