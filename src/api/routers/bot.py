from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from typing import Optional
from datetime import date, timedelta
from sqlmodel import Session
from src.database.database import get_session
from src.service.user_service import get_schedule_for_period
from src.service.admin_service import set_duty_report_by_date
from src.api.models import DutyDayReportUpdate

router = APIRouter(prefix="/bot", tags=["bot"])


@router.get("/schedule/today")
def get_schedule_today(session: Session = Depends(get_session)):
    today = date.today()
    duty_days = get_schedule_for_period(session, today, today)
    return duty_days[0] if duty_days else None


@router.get("/schedule/week")
def get_schedule_week(session: Session = Depends(get_session)):
    today = date.today()
    end = today + timedelta(days=7)
    return get_schedule_for_period(session, today, end)


@router.get("/schedule/month")
def get_schedule_month(session: Session = Depends(get_session)):
    today = date.today()
    end = today + timedelta(days=30)
    return get_schedule_for_period(session, today, end)


@router.post("/send_report")
def bot_send_report(
    duty_date: date = Form(...),
    report_room_number: int = Form(...),
    is_done: bool = Form(...),
    photo: Optional[UploadFile] = File(default=None),
    session: Session = Depends(get_session),
):
    photo_file = None
    content_type = None
    if photo is not None:
        photo_file = photo.file.read()
        content_type = photo.content_type

    update_data = DutyDayReportUpdate(
        duty_date=duty_date, report_room_number=report_room_number, is_done=is_done
    )

    try:
        return set_duty_report_by_date(session, update_data, photo_file, content_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
