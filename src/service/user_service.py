from datetime import date
from typing import List
from sqlmodel import Session, select
from src.database.models import DutyDay
from src.api.models import DutyDayRead


def get_schedule_for_period(
    session: Session, start: date, end: date
) -> List[DutyDayRead]:
    results = session.exec(
        select(DutyDay).where(DutyDay.duty_date >= start, DutyDay.duty_date <= end)
    ).all()
    duty_days = []
    for dd in results:
        room_nums = [dr.room_number for dr in dd.rooms]
        duty_days.append(
            DutyDayRead(duty_date=dd.duty_date, floor=dd.floor, rooms=room_nums)
        )
    return duty_days
