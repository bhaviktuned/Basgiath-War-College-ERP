from datetime import date as date_type, datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from .constants import QUADRANT_NAMES


class SignupRequest(BaseModel):
    name: str = Field(min_length=1)
    year: Optional[int] = None
    semester: Optional[int] = None
    branch: str  # must be one of the four quadrants
    section: Optional[str] = None
    email: EmailStr
    password: str = Field(min_length=8)

    @field_validator("branch")
    @classmethod
    def branch_must_be_a_quadrant(cls, v: str) -> str:
        if v not in QUADRANT_NAMES:
            raise ValueError(f"branch must be one of: {', '.join(QUADRANT_NAMES)}")
        return v


class LoginRequest(BaseModel):
    erp_id: str = Field(min_length=1)
    password: str


class UserOut(BaseModel):
    erp_id: str
    name: str
    email: str
    role: str
    year: Optional[int] = None
    semester: Optional[int] = None
    branch: Optional[str] = None
    section: Optional[str] = None
    elective_slot1: Optional[str] = None
    elective_slot2: Optional[str] = None

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class RosterStudentOut(BaseModel):
    erp_id: str
    name: str
    branch: Optional[str] = None

    class Config:
        from_attributes = True


class AttendanceEntryIn(BaseModel):
    erp_id: str
    status: Literal["present", "absent", "no_class"]


class AttendanceSessionCreate(BaseModel):
    subject: str = Field(min_length=1)
    date: date_type
    lecture_time: Optional[str] = None
    entries: List[AttendanceEntryIn]


class AttendanceSessionOut(BaseModel):
    subject: str
    date: date_type
    lecture_time: Optional[str] = None
    marked_count: int


class SubjectAttendanceSummary(BaseModel):
    subject: str
    present: int
    absent: int
    total: int
    percentage: float


class AttendanceSessionLogOut(BaseModel):
    date: date_type
    lecture_time: Optional[str] = None
    status: str


class CalendarEventOut(BaseModel):
    date: date_type
    title: str
    type: str

    class Config:
        from_attributes = True


class NoticeCreate(BaseModel):
    title: str = Field(min_length=1)
    body: str = Field(min_length=1)


class NoticeOut(BaseModel):
    id: int
    title: str
    body: str
    created_at: datetime

    class Config:
        from_attributes = True


class AssignmentCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    quadrant: Optional[str] = None
    subject: Optional[str] = None
    due_date: Optional[date_type] = None

    @field_validator("quadrant")
    @classmethod
    def quadrant_must_be_valid(cls, v):
        if v is not None and v not in QUADRANT_NAMES:
            raise ValueError(f"quadrant must be one of: {', '.join(QUADRANT_NAMES)}")
        return v


class AssignmentOut(BaseModel):
    id: int
    title: str
    description: str
    quadrant: Optional[str] = None
    subject: Optional[str] = None
    due_date: Optional[date_type] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ExamResultCreate(BaseModel):
    student_erp_id: str
    exam_name: str = Field(min_length=1)
    subject: str = Field(min_length=1)
    marks: float = Field(ge=0)
    max_marks: float = Field(gt=0, default=100)


class ExamResultOut(BaseModel):
    id: int
    exam_name: str
    subject: str
    marks: float
    max_marks: float
    created_at: datetime

    class Config:
        from_attributes = True


TIMETABLE_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TIMETABLE_TYPES = ["theory", "practical", "training", "laboratory", "review"]


class TimetableEntryOut(BaseModel):
    id: int
    quadrant: str
    day: str
    subject: str
    start_time: str
    end_time: str
    type: str
    room: Optional[str] = None
    year: Optional[int] = None

    class Config:
        from_attributes = True


class TimetableEntryCreate(BaseModel):
    quadrant: str
    day: str
    subject: str = Field(min_length=1)
    start_time: str = Field(min_length=1)
    end_time: str = Field(min_length=1)
    type: str = "theory"
    room: Optional[str] = None
    year: Optional[int] = None

    @field_validator("quadrant")
    @classmethod
    def quadrant_valid(cls, v):
        if v not in QUADRANT_NAMES:
            raise ValueError(f"quadrant must be one of: {', '.join(QUADRANT_NAMES)}")
        return v

    @field_validator("day")
    @classmethod
    def day_valid(cls, v):
        if v not in TIMETABLE_DAYS:
            raise ValueError(f"day must be one of: {', '.join(TIMETABLE_DAYS)}")
        return v

    @field_validator("type")
    @classmethod
    def type_valid(cls, v):
        if v not in TIMETABLE_TYPES:
            raise ValueError(f"type must be one of: {', '.join(TIMETABLE_TYPES)}")
        return v

class CourseRegistrationStatus(BaseModel):
    registered: bool
    core: List[str]
    electives: List[List[str]]  # each inner list is [optionA, optionB] for that slot
    elective_slot1: Optional[str] = None
    elective_slot2: Optional[str] = None
    subjects: List[str]  # core + chosen electives, once registered (else = core only)


class CourseRegistrationChoice(BaseModel):
    elective_slot1: str = Field(min_length=1)
    elective_slot2: str = Field(min_length=1)
