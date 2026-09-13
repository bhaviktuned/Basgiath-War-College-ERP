from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_user, require_faculty

router = APIRouter(prefix="/api/exam-results", tags=["exam-results"])


@router.get("", response_model=List[schemas.ExamResultOut])
def get_my_results(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Exam results are only tracked for students")
    return (
        db.query(models.ExamResult)
        .filter(models.ExamResult.user_id == current_user.id)
        .order_by(models.ExamResult.created_at.desc())
        .all()
    )


@router.post("", response_model=schemas.ExamResultOut, status_code=201)
def add_result(
    payload: schemas.ExamResultCreate,
    current_user: models.User = Depends(require_faculty),
    db: Session = Depends(get_db),
):
    student = db.query(models.User).filter(models.User.erp_id == payload.student_erp_id).first()
    if not student or student.role != "student":
        raise HTTPException(status_code=404, detail="Student not found")

    result = models.ExamResult(
        user_id=student.id,
        exam_name=payload.exam_name,
        subject=payload.subject,
        marks=payload.marks,
        max_marks=payload.max_marks,
        posted_by_id=current_user.id,
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result
