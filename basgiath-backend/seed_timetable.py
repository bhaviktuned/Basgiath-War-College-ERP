"""
Run once after setting up your database to populate the weekly timetable:

    python seed_timetable.py

Safe to re-run — it wipes and rebuilds the whole timetable table each time,
so edit the SCHEDULE below and re-run to update it.
"""
from app.database import Base, SessionLocal, engine
from app.models import TimetableEntry
from app.constants import QUADRANTS

Base.metadata.create_all(bind=engine)

ROOMS = {
    "Rider Quadrant": "Flight Deck & Roost",
    "Healer Quadrant": "Infirmary Hall",
    "Scribe Quadrant": "Archive Hall",
    "Infantry Quadrant": "Training Yard",
}


def classify_type(subject: str) -> str:
    s = subject.lower()
    if any(k in s for k in ["debrief", "review", "maintenance", "independent research", "practicum"]):
        return "review"
    if any(k in s for k in [
        "combat", "weapons", "aerial", "physical conditioning", "hand-to-hand",
        "riding", "reconnaissance", "formation", "siege", "ground tactics",
    ]):
        return "training"
    if any(k in s for k in ["surgery", "healing", "triage", "herbalism", "antidotes"]):
        return "practical"
    return "theory"


# (start, end, subject) — subject may be "A / B" for an elective choice slot,
# which gets split into two rows (one per option) at seed time.
SCHEDULE = {
    "Rider Quadrant": {
        "Monday": [
            ("08:00", "09:00", "Dragon Lore & Bonding"),
            ("09:00", "10:00", "Battle Strategy"),
            ("10:00", "10:15", "Break"),
            ("10:15", "12:15", "Weapons Training"),
            ("12:15", "13:00", "Lunch"),
            ("13:00", "14:00", "Aerial Combat"),
            ("14:00", "15:00", "Dragon Lore & Bonding"),
            ("15:00", "15:15", "Break"),
            ("15:15", "17:15", "Advanced Dragon Riding / Aerial Reconnaissance"),
            ("17:15", "18:00", "Tactical Debrief"),
        ],
        "Tuesday": [
            ("08:00", "10:00", "Aerial Combat"),
            ("10:00", "10:15", "Break"),
            ("10:15", "11:15", "Battle Strategy"),
            ("11:15", "12:15", "Dragon Lore & Bonding"),
            ("12:15", "13:00", "Lunch"),
            ("13:00", "15:00", "Survival & Fieldcraft / Tactical Leadership"),
            ("15:00", "15:15", "Break"),
            ("15:15", "17:15", "Weapons Training"),
            ("17:15", "18:00", "Tactical Debrief"),
        ],
        "Wednesday": [
            ("08:00", "09:00", "Battle Strategy"),
            ("09:00", "10:00", "Dragon Lore & Bonding"),
            ("10:00", "10:15", "Break"),
            ("10:15", "12:15", "Advanced Dragon Riding / Aerial Reconnaissance"),
            ("12:15", "13:00", "Lunch"),
            ("13:00", "15:00", "Aerial Combat"),
            ("15:00", "15:15", "Break"),
            ("15:15", "17:15", "Survival & Fieldcraft / Tactical Leadership"),
            ("17:15", "18:00", "Weapons Maintenance"),
        ],
        "Thursday": [
            ("08:00", "10:00", "Weapons Training"),
            ("10:00", "10:15", "Break"),
            ("10:15", "11:15", "Battle Strategy"),
            ("11:15", "12:15", "Dragon Lore & Bonding"),
            ("12:15", "13:00", "Lunch"),
            ("13:00", "15:00", "Aerial Combat"),
            ("15:00", "15:15", "Break"),
            ("15:15", "17:15", "Advanced Dragon Riding / Aerial Reconnaissance"),
            ("17:15", "18:00", "Tactical Debrief"),
        ],
        "Friday": [
            ("08:00", "09:00", "Dragon Lore & Bonding"),
            ("09:00", "10:00", "Battle Strategy"),
            ("10:00", "10:15", "Break"),
            ("10:15", "12:15", "Survival & Fieldcraft / Tactical Leadership"),
            ("12:15", "13:00", "Lunch"),
            ("13:00", "15:00", "Weapons Training"),
            ("15:00", "15:15", "Break"),
            ("15:15", "17:15", "Aerial Combat"),
            ("17:15", "18:00", "Weekly Combat Review"),
        ],
    },
    "Healer Quadrant": {
        "Monday": [
            ("08:00", "09:00", "Anatomy & Physiology"),
            ("09:00", "10:00", "Battlefield Medicine"),
            ("10:00", "10:15", "Break"),
            ("10:15", "12:15", "Field Surgery"),
            ("12:15", "13:00", "Lunch"),
            ("13:00", "14:00", "Combat Triage"),
            ("14:00", "15:00", "Emergency Response"),
            ("15:00", "15:15", "Break"),
            ("15:15", "17:15", "Advanced Healing Techniques"),
            ("17:15", "18:00", "Medical Records & Review"),
        ],
        "Tuesday": [
            ("08:00", "10:00", "Anatomy & Physiology"),
            ("10:00", "10:15", "Break"),
            ("10:15", "11:15", "Herbalism"),
            ("11:15", "12:15", "Battlefield Medicine"),
            ("12:15", "13:00", "Lunch"),
            ("13:00", "15:00", "Combat Triage"),
            ("15:00", "15:15", "Break"),
            ("15:15", "17:15", "Poisons & Antidotes"),
            ("17:15", "18:00", "Case Review"),
        ],
        "Wednesday": [
            ("08:00", "09:00", "Emergency Response"),
            ("09:00", "10:00", "Anatomy & Physiology"),
            ("10:00", "10:15", "Break"),
            ("10:15", "12:15", "Advanced Healing Techniques"),
            ("12:15", "13:00", "Lunch"),
            ("13:00", "15:00", "Field Surgery"),
            ("15:00", "15:15", "Break"),
            ("15:15", "17:15", "Battlefield Medicine"),
            ("17:15", "18:00", "Medical Records & Review"),
        ],
        "Thursday": [
            ("08:00", "09:00", "Herbalism"),
            ("09:00", "10:00", "Battlefield Medicine"),
            ("10:00", "10:15", "Break"),
            ("10:15", "12:15", "Emergency Response"),
            ("12:15", "13:00", "Lunch"),
            ("13:00", "15:00", "Poisons & Antidotes"),
            ("15:00", "15:15", "Break"),
            ("15:15", "17:15", "Combat Triage"),
            ("17:15", "18:00", "Case Review"),
        ],
        "Friday": [
            ("08:00", "09:00", "Anatomy & Physiology"),
            ("09:00", "10:00", "Emergency Response"),
            ("10:00", "10:15", "Break"),
            ("10:15", "12:15", "Field Surgery"),
            ("12:15", "13:00", "Lunch"),
            ("13:00", "14:00", "Battlefield Medicine"),
            ("14:00", "15:00", "Herbalism / Advanced Healing Techniques"),
            ("15:00", "15:15", "Break"),
            ("15:15", "17:15", "Combat Triage"),
            ("17:15", "18:00", "Weekly Medical Review"),
        ],
    },
    "Scribe Quadrant": {
        "Monday": [
            ("08:00", "09:00", "History of Navarre"),
            ("09:00", "10:00", "Military History"),
            ("10:00", "10:15", "Break"),
            ("10:15", "11:45", "Research & Analysis"),
            ("11:45", "12:15", "Archives & Records"),
            ("12:15", "13:00", "Lunch"),
            ("13:00", "14:00", "Ancient Languages / Translation Studies"),
            ("14:00", "15:00", "History of Navarre"),
            ("15:00", "15:15", "Break"),
            ("15:15", "16:45", "Runes & Ancient Texts / Military Intelligence"),
            ("16:45", "18:00", "Independent Research"),
        ],
        "Tuesday": [
            ("08:00", "09:00", "Archives & Records"),
            ("09:00", "10:00", "Research & Analysis"),
            ("10:00", "10:15", "Break"),
            ("10:15", "11:45", "Ancient Languages / Translation Studies"),
            ("11:45", "12:15", "Military History"),
            ("12:15", "13:00", "Lunch"),
            ("13:00", "14:00", "Runes & Ancient Texts / Military Intelligence"),
            ("14:00", "15:00", "Archives & Records"),
            ("15:00", "15:15", "Break"),
            ("15:15", "16:45", "Research & Analysis"),
            ("16:45", "18:00", "Archive Practicum"),
        ],
        "Wednesday": [
            ("08:00", "09:00", "Military History"),
            ("09:00", "10:00", "History of Navarre"),
            ("10:00", "10:15", "Break"),
            ("10:15", "11:45", "Research & Analysis"),
            ("11:45", "12:15", "Archives & Records"),
            ("12:15", "13:00", "Lunch"),
            ("13:00", "14:30", "Ancient Languages / Translation Studies"),
            ("14:30", "15:00", "Break"),
            ("15:00", "16:30", "Runes & Ancient Texts / Military Intelligence"),
            ("16:30", "18:00", "Independent Research"),
        ],
        "Thursday": [
            ("08:00", "09:00", "Archives & Records"),
            ("09:00", "10:00", "Military History"),
            ("10:00", "10:15", "Break"),
            ("10:15", "11:45", "Runes & Ancient Texts / Military Intelligence"),
            ("11:45", "12:15", "Research & Analysis"),
            ("12:15", "13:00", "Lunch"),
            ("13:00", "14:00", "History of Navarre"),
            ("14:00", "15:00", "Ancient Languages / Translation Studies"),
            ("15:00", "15:15", "Break"),
            ("15:15", "16:45", "Research & Analysis"),
            ("16:45", "18:00", "Archive Practicum"),
        ],
        "Friday": [
            ("08:00", "09:00", "History of Navarre"),
            ("09:00", "10:00", "Archives & Records"),
            ("10:00", "10:15", "Break"),
            ("10:15", "11:45", "Military History"),
            ("11:45", "12:15", "Research & Analysis"),
            ("12:15", "13:00", "Lunch"),
            ("13:00", "14:30", "Ancient Languages / Translation Studies"),
            ("14:30", "15:00", "Break"),
            ("15:00", "16:30", "Runes & Ancient Texts / Military Intelligence"),
            ("16:30", "18:00", "Weekly Research Review"),
        ],
    },
    "Infantry Quadrant": {
        "Monday": [
            ("08:00", "10:00", "Physical Conditioning"),
            ("10:00", "10:15", "Break"),
            ("10:15", "12:15", "Weapons & Armament"),
            ("12:15", "13:00", "Lunch"),
            ("13:00", "14:00", "Ground Tactics"),
            ("14:00", "15:00", "Battlefield Strategy"),
            ("15:00", "15:15", "Break"),
            ("15:15", "17:15", "Hand-to-Hand Combat"),
            ("17:15", "18:00", "Equipment Maintenance"),
        ],
        "Tuesday": [
            ("08:00", "09:00", "Ground Tactics"),
            ("09:00", "10:00", "Battlefield Strategy"),
            ("10:00", "10:15", "Break"),
            ("10:15", "12:15", "Formation Tactics / Siege Warfare"),
            ("12:15", "13:00", "Lunch"),
            ("13:00", "15:00", "Physical Conditioning"),
            ("15:00", "15:15", "Break"),
            ("15:15", "17:15", "Weapons & Armament"),
            ("17:15", "18:00", "Tactical Review"),
        ],
        "Wednesday": [
            ("08:00", "10:00", "Hand-to-Hand Combat"),
            ("10:00", "10:15", "Break"),
            ("10:15", "11:15", "Ground Tactics"),
            ("11:15", "12:15", "Battlefield Strategy"),
            ("12:15", "13:00", "Lunch"),
            ("13:00", "15:00", "Weapons & Armament"),
            ("15:00", "15:15", "Break"),
            ("15:15", "17:15", "Formation Tactics / Siege Warfare"),
            ("17:15", "18:00", "Equipment Maintenance"),
        ],
        "Thursday": [
            ("08:00", "10:00", "Physical Conditioning"),
            ("10:00", "10:15", "Break"),
            ("10:15", "12:15", "Hand-to-Hand Combat"),
            ("12:15", "13:00", "Lunch"),
            ("13:00", "14:00", "Ground Tactics"),
            ("14:00", "15:00", "Battlefield Strategy"),
            ("15:00", "15:15", "Break"),
            ("15:15", "17:15", "Formation Tactics / Siege Warfare"),
            ("17:15", "18:00", "Tactical Review"),
        ],
        "Friday": [
            ("08:00", "09:00", "Weapons & Armament"),
            ("09:00", "10:00", "Ground Tactics"),
            ("10:00", "10:15", "Break"),
            ("10:15", "12:15", "Physical Conditioning"),
            ("12:15", "13:00", "Lunch"),
            ("13:00", "15:00", "Hand-to-Hand Combat"),
            ("15:00", "15:15", "Break"),
            ("15:15", "17:15", "Battlefield Strategy"),
            ("17:15", "18:00", "Weekly Combat Review"),
        ],
    },
}


def elective_pair_for(quadrant: str, combined_subject: str):
    """If combined_subject is 'A / B' and matches one of the quadrant's real
    elective pairs, return (a, b). Otherwise return None."""
    if " / " not in combined_subject:
        return None
    parts = [p.strip() for p in combined_subject.split(" / ")]
    for pair in QUADRANTS[quadrant]["electives"]:
        if set(pair) == set(parts):
            return pair
    return None


db = SessionLocal()
try:
    deleted = db.query(TimetableEntry).delete()
    count = 0
    for quadrant, days in SCHEDULE.items():
        room = ROOMS.get(quadrant)
        for day, blocks in days.items():
            for start, end, subject in blocks:
                if subject in ("Break", "Lunch"):
                    continue  # not a real class — the frontend renders the gap itself
                pair = elective_pair_for(quadrant, subject)
                subjects_to_insert = list(pair) if pair else [subject]
                for s in subjects_to_insert:
                    db.add(TimetableEntry(
                        quadrant=quadrant, day=day, subject=s,
                        start_time=start, end_time=end,
                        type=classify_type(s), room=room, year=None,
                    ))
                    count += 1
    db.commit()
    print(f"Wiped {deleted} old entries. Seeded {count} timetable entries.")
finally:
    db.close()
