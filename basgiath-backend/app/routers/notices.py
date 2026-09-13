from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_user, require_faculty

router = APIRouter(prefix="/api/notices", tags=["notices"])


@router.get("", response_model=List[schemas.NoticeOut])
def list_notices(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(models.Notice).order_by(models.Notice.created_at.desc()).all()


@router.post("", response_model=schemas.NoticeOut, status_code=201)
def create_notice(
    payload: schemas.NoticeCreate,
    current_user: models.User = Depends(require_faculty),
    db: Session = Depends(get_db),
):
    notice = models.Notice(title=payload.title, body=payload.body, posted_by_id=current_user.id)
    db.add(notice)
    db.commit()
    db.refresh(notice)
    return notice


@router.delete("/{notice_id}", status_code=204)
def delete_notice(
    notice_id: int,
    current_user: models.User = Depends(require_faculty),
    db: Session = Depends(get_db),
):
    notice = db.query(models.Notice).filter(models.Notice.id == notice_id).first()
    if notice:
        db.delete(notice)
        db.commit()
