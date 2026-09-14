"""
Run once after setting up your database to populate the academic calendar:

    python seed.py
"""
from datetime import date

from app.database import Base, SessionLocal, engine
from app.models import CalendarEvent

Base.metadata.create_all(bind=engine)

EVENTS = [
    (date(2026, 8, 3), "New Cadet Arrival Day", "ceremony"),
    (date(2026, 8, 4), "Registration & Documentation", "academic"),
    (date(2026, 8, 5), "Equipment & Uniform Issue", "academic"),
    (date(2026, 8, 6), "Quadrant Assignment Ceremony", "ceremony"),
    (date(2026, 8, 7), "College Orientation", "academic"),
    (date(2026, 8, 8), "Squad Formation & Introduction", "ceremony"),
    (date(2026, 8, 10), "Academic Term Begins", "academic"),
    (date(2026, 8, 17), "Basic Combat Training Begins", "academic"),
    (date(2026, 8, 24), "First Tactical Assessment", "trial"),
    (date(2026, 8, 31), "Monthly Cadet Evaluation", "academic"),

    (date(2026, 9, 7), "Weapons Training Begins", "academic"),
    (date(2026, 9, 14), "Hand-to-Hand Combat Assessment", "trial"),
    (date(2026, 9, 21), "Tactical Strategy Exercise", "trial"),
    (date(2026, 9, 25), "First-Year Combat Evaluation", "trial"),
    (date(2026, 9, 28), "Squad Performance Assessment", "academic"),
    (date(2026, 9, 30), "September Progress Review", "academic"),

    (date(2026, 10, 5), "Dragon Studies Term Begins", "academic"),
    (date(2026, 10, 12), "Dragon Lore & Bonding Theory", "academic"),
    (date(2026, 10, 19), "Aerial Tactics Training Begins", "academic"),
    (date(2026, 10, 23), "Rider Aptitude Assessment", "trial"),
    (date(2026, 10, 26), "Survival Training Begins", "academic"),
    (date(2026, 10, 30), "Monthly Combat Assessment", "trial"),

    (date(2026, 11, 2), "Gauntlet Preparation Begins", "academic"),
    (date(2026, 11, 9), "Gauntlet Training Week", "academic"),
    (date(2026, 11, 16), "Tactical Trial", "trial"),
    (date(2026, 11, 20), "Squad Challenge", "trial"),
    (date(2026, 11, 23), "THE GAUNTLET", "trial"),
    (date(2026, 11, 24), "Gauntlet Results & Evaluation", "academic"),
    (date(2026, 11, 30), "Post-Gauntlet Assessment", "academic"),

    (date(2026, 12, 1), "Mid-Year Examination Period Begins", "academic"),
    (date(2026, 12, 7), "Academic Examinations", "academic"),
    (date(2026, 12, 11), "Practical Examinations", "trial"),
    (date(2026, 12, 14), "Combat Assessments", "trial"),
    (date(2026, 12, 17), "Squad Evaluations", "academic"),
    (date(2026, 12, 18), "Mid-Year Results Released", "academic"),
    (date(2026, 12, 19), "Winter Recess Begins", "ceremony"),

    (date(2027, 1, 4), "College Reopens", "ceremony"),
    (date(2027, 1, 5), "Cadet Return & Registration", "academic"),
    (date(2027, 1, 6), "Second Training Term Begins", "academic"),
    (date(2027, 1, 11), "Physical Conditioning Term Begins", "academic"),
    (date(2027, 1, 18), "Advanced Combat Training", "academic"),
    (date(2027, 1, 25), "Tactical Assessment", "trial"),

    (date(2027, 2, 1), "Advanced Quadrant Training Begins", "academic"),
    (date(2027, 2, 8), "Specialized Combat Training", "academic"),
    (date(2027, 2, 15), "Leadership Assessment", "trial"),
    (date(2027, 2, 19), "Aerial Combat Assessment", "trial"),
    (date(2027, 2, 22), "Squad Tactical Exercise", "trial"),
    (date(2027, 2, 26), "Monthly Performance Review", "academic"),

    (date(2027, 3, 1), "Field Training Preparation", "academic"),
    (date(2027, 3, 8), "Navigation & Survival Training", "academic"),
    (date(2027, 3, 15), "Wilderness Field Exercise", "trial"),
    (date(2027, 3, 19), "Squad Mission Simulation", "trial"),
    (date(2027, 3, 22), "Extended Field Exercise", "trial"),
    (date(2027, 3, 26), "Field Training Assessment", "trial"),
    (date(2027, 3, 29), "Recovery & Evaluation Week", "academic"),

    (date(2027, 4, 5), "War Games Preparation", "academic"),
    (date(2027, 4, 12), "Inter-Quadrant Tactical Trials", "trial"),
    (date(2027, 4, 16), "Aerial Competition", "trial"),
    (date(2027, 4, 19), "Squad Combat Trials", "trial"),
    (date(2027, 4, 23), "WAR GAMES — FINAL ROUND", "trial"),
    (date(2027, 4, 24), "War Games Results", "academic"),
    (date(2027, 4, 26), "Leadership & Strategy Review", "academic"),
    (date(2027, 4, 30), "College-Wide Performance Review", "academic"),

    (date(2027, 5, 3), "Final Examination Preparation Begins", "academic"),
    (date(2027, 5, 10), "Academic Revision Week", "academic"),
    (date(2027, 5, 17), "Written Final Examinations Begin", "academic"),
    (date(2027, 5, 21), "Practical Examination Period", "trial"),
    (date(2027, 5, 24), "Combat Final Assessments", "trial"),
    (date(2027, 5, 28), "Final Squad Evaluations", "academic"),
    (date(2027, 5, 31), "Final Examination Review", "academic"),

    (date(2027, 6, 1), "Final Trials Begin", "trial"),
    (date(2027, 6, 7), "Advanced Combat Trials", "trial"),
    (date(2027, 6, 11), "Leadership Trials", "trial"),
    (date(2027, 6, 14), "Dragon Rider Final Assessment", "trial"),
    (date(2027, 6, 18), "Tactical Command Assessment", "trial"),
    (date(2027, 6, 21), "Final Physical Evaluation", "trial"),
    (date(2027, 6, 24), "Fourth-Year Final Trials", "trial"),
    (date(2027, 6, 28), "Final Results Compilation", "academic"),
    (date(2027, 6, 30), "Final Results Released", "academic"),

    (date(2027, 7, 2), "Cadet Promotion Evaluations", "trial"),
    (date(2027, 7, 5), "Fourth-Year Graduation Rehearsal", "ceremony"),
    (date(2027, 7, 7), "Awards & Commendations", "ceremony"),
    (date(2027, 7, 9), "GRADUATION CEREMONY", "ceremony"),
    (date(2027, 7, 12), "Fourth-Year Departure", "ceremony"),
    (date(2027, 7, 15), "Promotion Ceremony", "ceremony"),
    (date(2027, 7, 19), "Academic Year Closure", "academic"),
    (date(2027, 7, 20), "Faculty Evaluation Period", "academic"),
    (date(2027, 7, 30), "New Academic Year Preparation", "academic"),
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
