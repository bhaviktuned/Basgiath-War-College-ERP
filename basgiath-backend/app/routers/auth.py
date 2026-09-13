from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..auth_utils import (
    create_access_token,
    generate_erp_id,
    hash_password,
    verify_password,
)
from ..database import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/signup", response_model=schemas.AuthResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: schemas.SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists")

    # Public signup only ever creates cadet (student) accounts. Faculty/admin
    # accounts are hardcoded and seeded at startup — see main.py.
    role = "student"

    if payload.year is None or payload.semester is None:
        raise HTTPException(
            status_code=422,
            detail="Year and semester are required for cadet sign-up",
        )

    erp_id = generate_erp_id(db, role)

    user = models.User(
        erp_id=erp_id,
        name=payload.name,
        email=str(payload.email).lower(),
        password_hash=hash_password(payload.password),
        role=role,
        year=payload.year,
        semester=payload.semester,
        branch=payload.branch,
        section=payload.section,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # No attendance is seeded here anymore. A cadet has no subjects — and
    # therefore no attendance ledger — until they complete Course Registration
    # (see routers/course_registration.py), which picks their electives and
    # creates the attendance records at that point.

    token = create_access_token({"sub": user.email, "erp_id": user.erp_id, "role": user.role})
    return schemas.AuthResponse(access_token=token, user=schemas.UserOut.model_validate(user))


@router.post("/login", response_model=schemas.AuthResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    invalid = HTTPException(status_code=401, detail="Incorrect ERP ID or password")

    user = db.query(models.User).filter(models.User.erp_id == payload.erp_id.strip()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise invalid

    token = create_access_token({"sub": user.email, "erp_id": user.erp_id, "role": user.role})
    return schemas.AuthResponse(access_token=token, user=schemas.UserOut.model_validate(user))
