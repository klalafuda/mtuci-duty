from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List
from sqlmodel import Session
from src.database.database import get_session
from src.api.models import DutyDayCreate
from src.service.admin_service import (
    list_duty_days,
    get_duty_day,
    create_duty_day,
    update_duty_day,
    delete_duty_day,
    set_duty_report,
)


def get_current_admin_user():
    return True


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/duty_days")
def admin_list_duty_days(
    session: Session = Depends(get_session), admin=Depends(get_current_admin_user)
):
    return list_duty_days(session)


@router.get("/duty_days/{duty_day_id}")
def admin_get_duty_day(
    duty_day_id: int,
    session: Session = Depends(get_session),
    admin=Depends(get_current_admin_user),
):
    dd = get_duty_day(session, duty_day_id)
    if dd is None:
        raise HTTPException(status_code=404, detail="Duty day not found")
    return dd


@router.post("/duty_days")
def admin_create_duty_day_api(
    data: DutyDayCreate,
    session: Session = Depends(get_session),
    admin=Depends(get_current_admin_user),
):
    try:
        return create_duty_day(session, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/duty_days/{duty_day_id}")
def admin_update_duty_day_api(
    duty_day_id: int,
    data: DutyDayCreate,
    session: Session = Depends(get_session),
    admin=Depends(get_current_admin_user),
):
    try:
        return update_duty_day(session, duty_day_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/duty_days/{duty_day_id}", status_code=204)
def admin_delete_duty_day_api(
    duty_day_id: int,
    session: Session = Depends(get_session),
    admin=Depends(get_current_admin_user),
):
    try:
        delete_duty_day(session, duty_day_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return


@router.post("/duty_days/{duty_day_id}/report")
async def admin_set_duty_report_api(
    duty_day_id: int,
    is_done: bool = Form(...),
    photos: List[UploadFile] = File(default=[]),
    session: Session = Depends(get_session),
    admin=Depends(get_current_admin_user),
):
    # Загрузим файлы в память. В реальном мире лучше стримить,
    # но здесь для простоты:
    photo_files = []
    content_types = []
    for f in photos:
        data = await f.read()
        photo_files.append(data)
        content_types.append(f.content_type)

    try:
        return set_duty_report(
            session, duty_day_id, is_done, photo_files, content_types
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
