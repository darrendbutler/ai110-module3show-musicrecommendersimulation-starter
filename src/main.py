"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


# Stress-test profiles. Same keys as user_prefs in main(); tempo is (bpm - 60) / 92.
HIGH_ENERGY_POP = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.90,         # workout / party intensity
    "target_valence": 0.85,        # bright and upbeat
    "target_danceability": 0.85,   # made for dancing
    "target_acousticness": 0.10,   # polished, electronic production
    "target_tempo": 0.74,          # ~128 BPM
}

CHILL_LOFI = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.30,         # barely-there background music
    "target_valence": 0.55,        # calm, neutral
    "target_danceability": 0.55,   # slow head-nod groove
    "target_acousticness": 0.80,   # warm, organic textures
    "target_tempo": 0.15,          # ~74 BPM
}

DEEP_INTENSE_ROCK = {
    "favorite_genre": "rock",
    "favorite_mood": "intense",
    "target_energy": 0.92,         # loud and driving
    "target_valence": 0.35,        # dark, aggressive tone
    "target_danceability": 0.50,   # headbang, not dance
    "target_acousticness": 0.08,   # distorted, amplified
    "target_tempo": 0.85,          # ~138 BPM
}


LATE_NIGHT_STUDY = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.40,         # low-key, background-friendly
    "target_valence": 0.58,        # neutral-to-slightly-positive
    "target_danceability": 0.60,   # gentle groove, not a dance floor
    "target_acousticness": 0.75,   # prefers organic/warm textures
    "target_tempo": 0.22,          # ~80 BPM, scaled as (bpm - 60) / 92
}

PROFILES = {
    "Late-Night Study": LATE_NIGHT_STUDY,
    "High-Energy Pop": HIGH_ENERGY_POP,
    "Chill Lofi": CHILL_LOFI,
    "Deep Intense Rock": DEEP_INTENSE_ROCK,
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    width = 60
    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\n" + "=" * width)
        print(f"{'TOP RECOMMENDATIONS: ' + name:^{width}}")
        print("=" * width)
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            artist = song.get("artist", "")
            by = f" by {artist}" if artist else ""
            print(f"\n#{rank}  {song['title']}{by}")
            print(f"    Score: {score:.2f}")
            print("    Reasons:")
            for reason in explanation.split(", "):
                print(f"      - {reason}")
            print("-" * width)
        print()


if __name__ == "__main__":
    main()
