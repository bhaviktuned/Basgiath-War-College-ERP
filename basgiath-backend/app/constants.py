# Each quadrant has 4 fixed "core" subjects everyone in that quadrant takes,
# plus 2 elective slots — each slot is a choice between exactly two options.
# Course registration = picking one option per elective slot.
QUADRANTS = {
    "Rider Quadrant": {
        "core": [
            "Dragon Lore & Bonding",
            "Aerial Combat",
            "Weapons Training",
            "Battle Strategy",
        ],
        "electives": [
            ["Advanced Dragon Riding", "Aerial Reconnaissance"],
            ["Survival & Fieldcraft", "Tactical Leadership"],
        ],
    },
    "Healer Quadrant": {
        "core": [
            "Anatomy & Physiology",
            "Battlefield Medicine",
            "Emergency Response",
            "Combat Triage",
        ],
        "electives": [
            ["Herbalism", "Advanced Healing Techniques"],
            ["Poisons & Antidotes", "Field Surgery"],
        ],
    },
    "Scribe Quadrant": {
        "core": [
            "History of Navarre",
            "Military History",
            "Archives & Records",
            "Research & Analysis",
        ],
        "electives": [
            ["Ancient Languages", "Translation Studies"],
            ["Runes & Ancient Texts", "Military Intelligence"],
        ],
    },
    "Infantry Quadrant": {
        "core": [
            "Weapons & Armament",
            "Hand-to-Hand Combat",
            "Ground Tactics",
            "Physical Conditioning",
        ],
        "electives": [
            ["Formation Tactics", "Siege Warfare"],
            ["Battlefield Strategy", "Combat Leadership"],
        ],
    },
}

QUADRANT_NAMES = list(QUADRANTS.keys())

# Hardcoded faculty/admin accounts. These are NOT created through public signup —
# they're seeded into the database on startup (see main.py) so login works for them.
# Fine for a capstone demo; in a real deployment these would never live in source control.
ADMIN_ACCOUNTS = [
    {"name": "Bhavik Shukla", "email": "bhavik72007@gmail.com", "password": "bhavik@07"},
    {"name": "Avika Soni", "email": "avikasoni05@outlook.com", "password": "avika@23"},
]
