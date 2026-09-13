from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_user, require_faculty

router = APIRouter(prefix="/api/assignments", tags=["assignments"])


@router.get("", response_model=List[schemas.AssignmentOut])
def list_assignments(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(models.Assignment)
    if current_user.role == "student" and current_user.branch:
        q = q.filter(
            (models.Assignment.quadrant == current_user.branch)
            | (models.Assignment.quadrant.is_(None))
        )
    return q.order_by(models.Assignment.created_at.desc()).all()


@router.post("", response_model=schemas.AssignmentOut, status_code=201)
def create_assignment(
    payload: schemas.AssignmentCreate,
    current_user: models.User = Depends(require_faculty),
    db: Session = Depends(get_db),
):
    assignment = models.Assignment(
        title=payload.title,
        description=payload.description,
        quadrant=payload.quadrant,
        subject=payload.subject,
        due_date=payload.due_date,
        posted_by_id=current_user.id,
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


@router.delete("/{assignment_id}", status_code=204)
def delete_assignment(
    assignment_id: int,
    current_user: models.User = Depends(require_faculty),
    db: Session = Depends(get_db),
):
    assignment = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    if assignment:
        db.delete(assignment)
        db.commit()
