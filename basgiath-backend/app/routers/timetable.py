from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..constants import QUADRANTS, QUADRANT_NAMES
from ..database import get_db
from ..deps import get_current_user, require_faculty

router = APIRouter(prefix="/api/timetable", tags=["timetable"])

DAY_ORDER = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4}


def _sorted(entries):
    return sorted(entries, key=lambda e: (DAY_ORDER.get(e.day, 99), e.start_time))


@router.get("", response_model=List[schemas.TimetableEntryOut])
def get_my_timetable(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Student: their quadrant's full week, with only their chosen elective
    shown in each elective slot — the option they didn't pick is filtered out."""
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Use /api/timetable/quadrant/{name} for faculty browsing")
    if not current_user.branch or current_user.branch not in QUADRANTS:
        raise HTTPException(status_code=400, detail="Your account has no valid quadrant set")
    if not (current_user.elective_slot1 and current_user.elective_slot2):
        raise HTTPException(status_code=400, detail="Complete Course Registration first")

    entries = (
        db.query(models.TimetableEntry)
        .filter(models.TimetableEntry.quadrant == current_user.branch)
        .all()
    )

    chosen = {current_user.elective_slot1, current_user.elective_slot2}
    all_elective_options = set()
    for pair in QUADRANTS[current_user.branch]["electives"]:
        all_elective_options.update(pair)

    visible = []
    for e in entries:
        if e.subject in all_elective_options and e.subject not in chosen:
            continue  # the elective option this student did NOT pick
        if e.year is not None and current_user.year is not None and e.year != current_user.year:
            continue
        visible.append(e)

    return _sorted(visible)


@router.get("/quadrant/{quadrant}", response_model=List[schemas.TimetableEntryOut])
def get_quadrant_timetable(
    quadrant: str,
    current_user: models.User = Depends(require_faculty),
    db: Session = Depends(get_db),
):
    """Faculty/admin: the FULL schedule for a quadrant, both elective options included."""
    if quadrant not in QUADRANT_NAMES:
        raise HTTPException(status_code=404, detail="Unknown quadrant")
    entries = db.query(models.TimetableEntry).filter(models.TimetableEntry.quadrant == quadrant).all()
    return _sorted(entries)


@router.post("", response_model=schemas.TimetableEntryOut, status_code=201)
def create_entry(
    payload: schemas.TimetableEntryCreate,
    current_user: models.User = Depends(require_faculty),
    db: Session = Depends(get_db),
):
    entry = models.TimetableEntry(**payload.model_dump(), created_by_id=current_user.id)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.put("/{entry_id}", response_model=schemas.TimetableEntryOut)
def update_entry(
    entry_id: int,
    payload: schemas.TimetableEntryCreate,
    current_user: models.User = Depends(require_faculty),
    db: Session = Depends(get_db),
):
    entry = db.query(models.TimetableEntry).filter(models.TimetableEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    for key, value in payload.model_dump().items():
        setattr(entry, key, value)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{entry_id}", status_code=204)
def delete_entry(
    entry_id: int,
    current_user: models.User = Depends(require_faculty),
    db: Session = Depends(get_db),
):
    entry = db.query(models.TimetableEntry).filter(models.TimetableEntry.id == entry_id).first()
    if entry:
        db.delete(entry)
        db.commit()