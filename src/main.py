"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 
    # print("Loaded songs", songs)
    # Taste profile: "late-night study session" listener.
    # Keys mirror the UserProfile features in the README; numeric targets are 0-1.
    user_prefs = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,         # low-key, background-friendly
        "target_valence": 0.58,        # neutral-to-slightly-positive
        "target_danceability": 0.60,   # gentle groove, not a dance floor
        "target_acousticness": 0.75,   # prefers organic/warm textures
        "target_tempo": 0.22,          # ~80 BPM, scaled as (bpm - 60) / 92
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    width = 60
    print("\n" + "=" * width)
    print(f"{'TOP RECOMMENDATIONS':^{width}}")
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
