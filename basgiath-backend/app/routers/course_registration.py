from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..constants import QUADRANTS
from ..database import get_db
from ..deps import get_current_user

router = APIRouter(prefix="/api/course-registration", tags=["course-registration"])


def _require_student_with_quadrant(current_user: models.User):
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students register for courses")
    if not current_user.branch or current_user.branch not in QUADRANTS:
        raise HTTPException(status_code=400, detail="Your account has no valid quadrant set")


@router.get("", response_model=schemas.CourseRegistrationStatus)
def get_registration_status(
    current_user: models.User = Depends(get_current_user),
):
    _require_student_with_quadrant(current_user)
    quadrant = QUADRANTS[current_user.branch]
    registered = bool(current_user.elective_slot1 and current_user.elective_slot2)

    subjects = list(quadrant["core"])
    if registered:
        subjects += [current_user.elective_slot1, current_user.elective_slot2]

    return schemas.CourseRegistrationStatus(
        registered=registered,
        core=quadrant["core"],
        electives=quadrant["electives"],
        elective_slot1=current_user.elective_slot1,
        elective_slot2=current_user.elective_slot2,
        subjects=subjects,
    )


@router.post("", response_model=schemas.CourseRegistrationStatus)
def submit_registration(
    payload: schemas.CourseRegistrationChoice,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_student_with_quadrant(current_user)
    quadrant = QUADRANTS[current_user.branch]
    slot1_options, slot2_options = quadrant["electives"]

    if payload.elective_slot1 not in slot1_options:
        raise HTTPException(
            status_code=422,
            detail=f"elective_slot1 must be one of: {', '.join(slot1_options)}",
        )
    if payload.elective_slot2 not in slot2_options:
        raise HTTPException(
            status_code=422,
            detail=f"elective_slot2 must be one of: {', '.join(slot2_options)}",
        )

    current_user.elective_slot1 = payload.elective_slot1
    current_user.elective_slot2 = payload.elective_slot2

    # (Re-)registering resets the attendance ledger: wipe any prior sessions'
    # entries for this student, then mark them present for a "day one"
    # session in each of their final subjects. Real day-to-day tracking from
    # here on is done by faculty via /api/attendance/sessions.
    db.query(models.AttendanceEntry).filter(
        models.AttendanceEntry.student_id == current_user.id
    ).delete()

    final_subjects = list(quadrant["core"]) + [payload.elective_slot1, payload.elective_slot2]
    today = date.today()
    for subject in final_subjects:
        session = (
            db.query(models.AttendanceSession)
            .filter(
                models.AttendanceSession.subject == subject,
                models.AttendanceSession.date == today,
                models.AttendanceSession.lecture_time == "Registration Day",
            )
            .first()
        )
        if not session:
            session = models.AttendanceSession(
                subject=subject,
                date=today,
                lecture_time="Registration Day",
                created_by_id=current_user.id,
            )
            db.add(session)
            db.flush()
        db.add(
            models.AttendanceEntry(session_id=session.id, student_id=current_user.id, status="present")
        )

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return schemas.CourseRegistrationStatus(
        registered=True,
        core=quadrant["core"],
        electives=quadrant["electives"],
        elective_slot1=current_user.elective_slot1,
        elective_slot2=current_user.elective_slot2,
        subjects=final_subjects,
    )
