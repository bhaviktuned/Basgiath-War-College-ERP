from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import extract
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/calendar", tags=["calendar"])


@router.get("/events", response_model=List[schemas.CalendarEventOut])
def get_events(
    year: Optional[int] = Query(default=None),
    month: Optional[int] = Query(default=None, ge=1, le=12),
    db: Session = Depends(get_db),
):
    q = db.query(models.CalendarEvent)
    if year:
        q = q.filter(extract("year", models.CalendarEvent.date) == year)
    if month:
        q = q.filter(extract("month", models.CalendarEvent.date) == month)
    return q.order_by(models.CalendarEvent.date).all()
