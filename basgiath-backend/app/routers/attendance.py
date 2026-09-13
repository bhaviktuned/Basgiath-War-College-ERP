from collections import defaultdict
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..constants import QUADRANTS
from ..database import get_db
from ..deps import get_current_user, require_faculty

router = APIRouter(prefix="/api/attendance", tags=["attendance"])


def _student_subjects(student: models.User) -> set:
    """The final subject list (core + chosen electives) for a registered student."""
    if not student.branch or student.branch not in QUADRANTS:
        return set()
    quadrant = QUADRANTS[student.branch]
    subjects = set(quadrant["core"])
    if student.elective_slot1:
        subjects.add(student.elective_slot1)
    if student.elective_slot2:
        subjects.add(student.elective_slot2)
    return subjects


@router.get("/roster", response_model=List[schemas.RosterStudentOut])
def get_roster(
    subject: str,
    current_user: models.User = Depends(require_faculty),
    db: Session = Depends(get_db),
):
    """All registered students who take the given subject — for faculty to mark."""
    students = (
        db.query(models.User)
        .filter(models.User.role == "student", models.User.elective_slot1.isnot(None))
        .all()
    )
    roster = [s for s in students if subject in _student_subjects(s)]
    roster.sort(key=lambda s: s.name)
    return roster


@router.post("/sessions", response_model=schemas.AttendanceSessionOut, status_code=201)
def create_session(
    payload: schemas.AttendanceSessionCreate,
    current_user: models.User = Depends(require_faculty),
    db: Session = Depends(get_db),
):
    """Faculty: record a class session and mark every listed student present/absent.
    Re-submitting for the same subject/date/lecture_time updates that session
    instead of creating a duplicate."""
    session = (
        db.query(models.AttendanceSession)
        .filter(
            models.AttendanceSession.subject == payload.subject,
            models.AttendanceSession.date == payload.date,
            models.AttendanceSession.lecture_time == payload.lecture_time,
        )
        .first()
    )
    if not session:
        session = models.AttendanceSession(
            subject=payload.subject,
            date=payload.date,
            lecture_time=payload.lecture_time,
            created_by_id=current_user.id,
        )
        db.add(session)
        db.flush()
    else:
        # clean slate for this session, then re-mark from the submitted roster
        db.query(models.AttendanceEntry).filter(
            models.AttendanceEntry.session_id == session.id
        ).delete()

    marked = 0
    for entry in payload.entries:
        student = db.query(models.User).filter(models.User.erp_id == entry.erp_id).first()
        if not student or student.role != "student":
            continue
        db.add(
            models.AttendanceEntry(
                session_id=session.id, student_id=student.id, status=entry.status
            )
        )
        marked += 1

    db.commit()
    return schemas.AttendanceSessionOut(
        subject=session.subject,
        date=session.date,
        lecture_time=session.lecture_time,
        marked_count=marked,
    )


@router.get("", response_model=List[schemas.SubjectAttendanceSummary])
def get_my_attendance_summary(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Attendance is only tracked for students")

    entries = (
        db.query(models.AttendanceEntry, models.AttendanceSession)
        .join(models.AttendanceSession, models.AttendanceEntry.session_id == models.AttendanceSession.id)
        .filter(models.AttendanceEntry.student_id == current_user.id)
        .all()
    )

    counts = defaultdict(lambda: {"present": 0, "absent": 0, "no_class": 0})
    for entry, session in entries:
        counts[session.subject][entry.status] += 1

    summaries = []
    for subject, c in counts.items():
        total = c["present"] + c["absent"]  # "no_class" sessions don't count toward the percentage
        percentage = round((c["present"] / total) * 100, 1) if total else 0.0
        summaries.append(
            schemas.SubjectAttendanceSummary(
                subject=subject, present=c["present"], absent=c["absent"],
                total=total, percentage=percentage,
            )
        )
    summaries.sort(key=lambda s: s.subject)
    return summaries


@router.get("/{subject}/log", response_model=List[schemas.AttendanceSessionLogOut])
def get_my_subject_log(
    subject: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Attendance is only tracked for students")

    rows = (
        db.query(models.AttendanceEntry, models.AttendanceSession)
        .join(models.AttendanceSession, models.AttendanceEntry.session_id == models.AttendanceSession.id)
        .filter(
            models.AttendanceEntry.student_id == current_user.id,
            models.AttendanceSession.subject == subject,
        )
        .order_by(models.AttendanceSession.date.desc())
        .all()
    )
    return [
        schemas.AttendanceSessionLogOut(
            date=session.date, lecture_time=session.lecture_time, status=entry.status
        )
        for entry, session in rows
    ]
