from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    erp_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    # "student" for everyone who signs up through the portal.
    # "faculty" only exists for the two hardcoded admin accounts seeded at startup.
    role = Column(String, nullable=False, default="student")

    year = Column(Integer, nullable=True)
    semester = Column(Integer, nullable=True)
    branch = Column(String, nullable=True)  # quadrant name, e.g. "Rider Quadrant"
    section = Column(String, nullable=True)

    # Course registration: one chosen subject per elective slot. Both are set
    # together, at registration time — null means "hasn't registered yet".
    elective_slot1 = Column(String, nullable=True)
    elective_slot2 = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    attendance_entries = relationship(
        "AttendanceEntry", back_populates="student", cascade="all, delete-orphan"
    )
    exam_results = relationship(
        "ExamResult", back_populates="user", cascade="all, delete-orphan",
        foreign_keys="ExamResult.user_id",
    )


class AttendanceSession(Base):
    """One taken class — a specific subject, on a specific date/time slot.
    Faculty create these and mark each enrolled student present or absent."""
    __tablename__ = "attendance_sessions"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=False, index=True)
    date = Column(Date, nullable=False)
    lecture_time = Column(String, nullable=True)  # e.g. "10:00 AM - 10:50 AM"
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    entries = relationship(
        "AttendanceEntry", back_populates="session", cascade="all, delete-orphan"
    )


class AttendanceEntry(Base):
    """One student's present/absent mark for one AttendanceSession."""
    __tablename__ = "attendance_entries"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("attendance_sessions.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, nullable=False)  # "present" | "absent"

    session = relationship("AttendanceSession", back_populates="entries")
    student = relationship("User", back_populates="attendance_entries")


class CalendarEvent(Base):
    __tablename__ = "calendar_events"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False, default="academic")  # trial | ceremony | academic


class Notice(Base):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    posted_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    posted_by = relationship("User")


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    quadrant = Column(String, nullable=True)  # null = applies to all quadrants
    subject = Column(String, nullable=True)
    due_date = Column(Date, nullable=True)
    posted_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    posted_by = relationship("User")


class ExamResult(Base):
    __tablename__ = "exam_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exam_name = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    marks = Column(Float, nullable=False)
    max_marks = Column(Float, nullable=False, default=100)
    posted_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="exam_results", foreign_keys=[user_id])
