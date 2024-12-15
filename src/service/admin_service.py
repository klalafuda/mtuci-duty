from io import BytesIO

from sqlmodel import Session, select
from typing import Optional
from src.database.models import DutyDay, DutyRoom, Room
from src.api.models import DutyDayCreate, DutyDayRead, DutyDayReportUpdate
from src.service.storage_service import upload_file


def create_duty_day(session: Session, data: DutyDayCreate) -> DutyDayRead:
    existing = session.exec(
        select(DutyDay).where(DutyDay.duty_date == data.duty_date)
    ).first()
    if existing:
        raise ValueError("Duty day for this date already exists")

    rooms_in_db = session.exec(select(Room).where(Room.number.in_(data.rooms))).all()
    if len(rooms_in_db) != len(data.rooms):
        raise ValueError("One or more rooms do not exist")

    new_day = DutyDay(
        duty_date=data.duty_date, floor=data.floor, is_done=False, photo_url=None
    )
    session.add(new_day)
    session.commit()
    session.refresh(new_day)

    for rnum in data.rooms:
        dr = DutyRoom(duty_day_id=new_day.id, room_number=rnum)
        session.add(dr)

    session.commit()
    session.refresh(new_day)

    return DutyDayRead(
        duty_date=new_day.duty_date,
        floor=new_day.floor,
        is_done=new_day.is_done,
        photo_url=new_day.photo_url,
        rooms=[dr.room_number for dr in new_day.rooms],
        report_room_number=new_day.report_room_number,
    )


def update_duty_day(
    session: Session, duty_day_id: int, data: DutyDayCreate
) -> DutyDayRead:
    dd = session.get(DutyDay, duty_day_id)
    if not dd:
        raise ValueError("Duty day not found")

    existing = session.exec(
        select(DutyDay).where(
            DutyDay.duty_date == data.duty_date, DutyDay.id != duty_day_id
        )
    ).first()
    if existing:
        raise ValueError("Another duty day with this date already exists")

    rooms_in_db = session.exec(select(Room).where(Room.number.in_(data.rooms))).all()
    if len(rooms_in_db) != len(data.rooms):
        raise ValueError("One or more rooms do not exist")

    dd.duty_date = data.duty_date
    dd.floor = data.floor

    for old_dr in dd.rooms:
        session.delete(old_dr)
    session.commit()

    for rnum in data.rooms:
        dr = DutyRoom(duty_day_id=dd.id, room_number=rnum)
        session.add(dr)

    session.commit()
    session.refresh(dd)

    return DutyDayRead(
        duty_date=dd.duty_date,
        floor=dd.floor,
        is_done=dd.is_done,
        photo_url=dd.photo_url,
        rooms=[dr.room_number for dr in dd.rooms],
        report_room_number=dd.report_room_number,
    )


def delete_duty_day(session: Session, duty_day_id: int) -> None:
    dd = session.get(DutyDay, duty_day_id)
    if not dd:
        raise ValueError("Duty day not found")
    session.delete(dd)
    session.commit()


def list_duty_days(session: Session) -> list[DutyDayRead]:
    results = session.exec(select(DutyDay)).all()
    return [
        DutyDayRead(
            duty_date=dd.duty_date,
            floor=dd.floor,
            is_done=dd.is_done,
            photo_url=dd.photo_url,
            rooms=[dr.room_number for dr in dd.rooms],
            report_room_number=dd.report_room_number,
        )
        for dd in results
    ]


def get_duty_day(session: Session, duty_day_id: int) -> DutyDayRead | None:
    dd = session.get(DutyDay, duty_day_id)
    if not dd:
        return None
    return DutyDayRead(
        duty_date=dd.duty_date,
        floor=dd.floor,
        is_done=dd.is_done,
        photo_url=dd.photo_url,
        rooms=[dr.room_number for dr in dd.rooms],
        report_room_number=dd.report_room_number,
    )


def set_duty_report(
    session: Session,
    duty_day_id: int,
    is_done: bool,
    photo_file: bytes | None,
    content_type: str | None,
    report_room_number: int | None = None,
) -> DutyDayRead:
    dd = session.get(DutyDay, duty_day_id)

    photo_file: BytesIO | None = BytesIO(photo_file)

    if not dd:
        raise ValueError("Duty day not found")

    if photo_file is not None and content_type is not None:
        url = upload_file(file_data=photo_file, content_type=content_type)
        dd.photo_url = url

    dd.is_done = is_done
    if report_room_number is not None:
        dd.report_room_number = report_room_number

    session.commit()
    session.refresh(dd)
    return DutyDayRead(
        duty_date=dd.duty_date,
        floor=dd.floor,
        is_done=dd.is_done,
        photo_url=dd.photo_url,
        rooms=[dr.room_number for dr in dd.rooms],
        report_room_number=dd.report_room_number,
    )


def set_duty_report_by_date(
    session: Session,
    data: DutyDayReportUpdate,
    photo_file: bytes | None,
    content_type: str | None,
) -> DutyDayRead:
    photo_file: BytesIO | None = BytesIO(photo_file)

    dd = session.exec(
        select(DutyDay).where(DutyDay.duty_date == data.duty_date)
    ).first()
    if not dd:
        raise ValueError("Duty day not found for this date")

    if photo_file is not None and content_type is not None:
        url = upload_file(photo_file, content_type)
        dd.photo_url = url

    dd.is_done = data.is_done
    dd.report_room_number = data.report_room_number

    session.commit()
    session.refresh(dd)
    return DutyDayRead(
        duty_date=dd.duty_date,
        floor=dd.floor,
        is_done=dd.is_done,
        photo_url=dd.photo_url,
        rooms=[dr.room_number for dr in dd.rooms],
        report_room_number=dd.report_room_number,
    )
