"""
Run once after setting up your database to populate the academic calendar:

    python seed.py
"""
from datetime import date

from app.database import Base, SessionLocal, engine
from app.models import CalendarEvent

Base.metadata.create_all(bind=engine)

EVENTS = [
    (date(2026, 8, 3), "Presentation Day — Choosing Ceremony", "ceremony"),
    (date(2026, 8, 10), "The Threshing", "trial"),
    (date(2026, 9, 14), "Parapet Crossing", "trial"),
    (date(2026, 9, 28), "First War Games Exercise", "academic"),
    (date(2026, 10, 5), "The Gauntlet", "trial"),
    (date(2026, 10, 19), "Squad Rotation Assessments", "academic"),
    (date(2026, 11, 9), "Guest Briefing: History of Navarre", "academic"),
    (date(2026, 11, 23), "Midyear Vellum Exams", "academic"),
    (date(2026, 12, 7), "Flight Formation Trials", "trial"),
    (date(2026, 12, 20), "Winter Recess Begins", "ceremony"),
    (date(2027, 1, 12), "Spring Term Begins", "academic"),
    (date(2027, 1, 26), "Signet Manifestation Trials", "trial"),
    (date(2027, 2, 9), "Melee Week: Combat Rotations", "trial"),
    (date(2027, 2, 23), "War Council Briefing", "academic"),
    (date(2027, 3, 8), "The Reckoning (Second Gauntlet)", "trial"),
    (date(2027, 3, 22), "Dragon Bonding Review", "ceremony"),
    (date(2027, 4, 5), "Field Exercise: Mountain Survival", "trial"),
    (date(2027, 4, 19), "Vellum Finals Begin", "academic"),
    (date(2027, 5, 3), "Squad Championship Duels", "trial"),
    (date(2027, 5, 17), "Choosing of the Wingleaders", "ceremony"),
    (date(2027, 6, 7), "Graduation Flight", "ceremony"),
    (date(2027, 6, 21), "Commissioning Ceremony", "ceremony"),
    (date(2027, 7, 12), "Summer Rider Assignments Posted", "academic"),
]

db = SessionLocal()
try:
    if db.query(CalendarEvent).count() == 0:
        for event_date, title, event_type in EVENTS:
            db.add(CalendarEvent(date=event_date, title=title, type=event_type))
        db.commit()
        print(f"Seeded {len(EVENTS)} calendar events.")
    else:
        print("Calendar events already present — skipping seed.")
finally:
    db.close()
