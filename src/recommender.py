import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into dicts with numeric fields converted to int/float."""
    int_fields = ("id",)
    float_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

# Max points per feature from the README's Algorithm Recipe, with the weight-shift
# experiment applied: energy doubled (30 -> 60), genre halved (15 -> 7.5).
# The raw total is 122.5, so each weight is divided by 1.225 to keep scores on a
# 0-100 scale comparable to the pre-experiment version.
_RAW_WEIGHTS = {
    "energy": 60.0,
    "mood": 25.0,
    "genre": 7.5,
    "valence": 10.0,
    "acousticness": 10.0,
    "danceability": 5.0,
    "tempo": 5.0,
}
WEIGHTS = {name: w / 1.225 for name, w in _RAW_WEIGHTS.items()}

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song (0-100) against user preferences and return (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    # Categorical features: all-or-nothing bonus on an exact match.
    if song["mood"] == user_prefs["favorite_mood"]:
        score += WEIGHTS["mood"]
        reasons.append(f"mood match (+{WEIGHTS['mood']:.1f})")
    if song["genre"] == user_prefs["favorite_genre"]:
        score += WEIGHTS["genre"]
        reasons.append(f"genre match (+{WEIGHTS['genre']:.1f})")

    # Numeric features: linear closeness, weight * (1 - |song - target|).
    scaled_tempo = (song["tempo_bpm"] - 60) / 92
    numeric = [
        ("energy", song["energy"], user_prefs["target_energy"]),
        ("valence", song["valence"], user_prefs["target_valence"]),
        ("acousticness", song["acousticness"], user_prefs["target_acousticness"]),
        ("danceability", song["danceability"], user_prefs["target_danceability"]),
        ("tempo", scaled_tempo, user_prefs["target_tempo"]),
    ]
    for name, value, target in numeric:
        points = WEIGHTS[name] * (1 - abs(value - target))
        score += points
        reasons.append(f"{name} closeness (+{points:.1f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top-k (song, score, explanation) tuples ranked by score against user preferences."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, ", ".join(reasons)))

    # Highest score first; ties break on energy closeness, then title (per README).
    scored.sort(key=lambda r: (-r[1], abs(r[0]["energy"] - user_prefs["target_energy"]), r[0]["title"]))
    return scored[:k]
