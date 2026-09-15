from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .auth_utils import generate_erp_id, hash_password
from .constants import ADMIN_ACCOUNTS
from .database import Base, SessionLocal, engine
from .routers import assignments, attendance, auth, calendar, course_registration, exam, meta, notices, profile, timetable

Base.metadata.create_all(bind=engine)


def seed_admin_accounts():
    """Ensure the two hardcoded faculty/admin accounts exist. Idempotent —
    safe to run on every startup. These accounts can never be created or
    modified through the public signup form."""
    db = SessionLocal()
    try:
        for account in ADMIN_ACCOUNTS:
            existing = db.query(models.User).filter(models.User.email == account["email"]).first()
            if existing:
                continue
            user = models.User(
                erp_id=generate_erp_id(db, "faculty"),
                name=account["name"],
                email=account["email"].lower(),
                password_hash=hash_password(account["password"]),
                role="faculty",
            )
            db.add(user)
            db.flush()  # make this row visible to generate_erp_id() for the next admin in the loop
        db.commit()
    finally:
        db.close()


seed_admin_accounts()

app = FastAPI(title="Basgiath War College — Rider Portal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this to your frontend's origin before going live
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(meta.router)
app.include_router(attendance.router)
app.include_router(course_registration.router)
app.include_router(calendar.router)
app.include_router(notices.router)
app.include_router(assignments.router)
app.include_router(exam.router)
app.include_router(timetable.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
