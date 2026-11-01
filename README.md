# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

<!-- Response -->

Real-world recommenders like Spotify and YouTube combine many signals: what a listener plays, skips, saves, and repeats, what similar listeners enjoy (collaborative filtering), and the attributes of the songs themselves (content-based filtering). They score a huge pool of candidates and then rank them, adding rules such as variety and freshness on top. This simulation keeps only the content-based part. Each song is compared against a user's taste profile using simple linear similarity, `1 - |song_value - target_value|`, so a song scores highest when it is *closest* to what the user wants rather than simply higher or lower. The system scores numeric features (energy, acousticness, valence, danceability, and tempo, with tempo scaled to 0-1) this way, and adds a bonus when a song's mood or genre matches the user's. Energy and mood carry the most weight, since they best capture a listening context, while genre, danceability, and tempo carry less because they are sparse or largely overlap with energy. Every song gets one score, and the recommender then ranks the songs from highest to lowest and returns the top results.

**`Song` features** (one per row of `data/songs.csv`):

- Identifiers (not scored): `id`, `title`, `artist`
- Categorical: `genre`, `mood`
- Numeric, 0-1: `energy`, `valence`, `danceability`, `acousticness`
- Numeric, scaled to 0-1 before scoring: `tempo_bpm` (`(bpm - 60) / 92`)

**`UserProfile` features** (the user's taste profile, mirroring the scored song features):

- Categorical: `favorite_genre`, `favorite_mood`
- Numeric targets, 0-1: `target_energy`, `target_valence`, `target_danceability`, `target_acousticness`
- Numeric target, scaled to 0-1: `target_tempo`

Each numeric target is compared with the matching song feature using linear similarity, and each categorical preference earns a bonus on an exact match.

### Algorithm Recipe

Every song in `data/songs.csv` is scored out of 100 points. The score is the sum of the points below:

| Feature | Max points | How it is scored |
|---|---|---|
| Energy | 30 | `30 × (1 - abs(song.energy - target_energy))` |
| Mood | 25 | `25` if `song.mood == favorite_mood`, otherwise `0` |
| Genre | 15 | `15` if `song.genre == favorite_genre`, otherwise `0` |
| Valence | 10 | `10 × (1 - abs(song.valence - target_valence))` |
| Acousticness | 10 | `10 × (1 - abs(song.acousticness - target_acousticness))` |
| Danceability | 5 | `5 × (1 - abs(song.danceability - target_danceability))` |
| Tempo | 5 | `5 × (1 - abs(scaled_tempo - target_tempo))`, with `scaled_tempo = (bpm - 60) / 92` |

The steps:

1. **Input:** read the user's taste profile and load every row of `data/songs.csv` as a `Song`.
2. **Process (the loop):** for each song, compute the seven point values above, add them up, and keep the total with a short list of reasons (for example, "mood match +25, energy +28.4").
3. **Output:** sort all songs by total score, highest first, break ties by energy closeness and then title, and return the top `k` with their scores and reasons.

The flow is diagrammed in [diagram/score_logic.mmd](diagram/score_logic.mmd).

The weights are a starting point. They are kept in one `WEIGHTS` dictionary so they are easy to change in the experiments.

### Expected Biases

- **Sparse catalog makes categorical matches rare.** Only lofi appears more than once among the 20 songs, so a genre match usually applies to a single song. Genre is capped at 15 points to keep it from acting as a hard filter, but any song that does match gets a visible boost over equally good songs in a neighboring genre (for example, indie pop vs. pop).
- **Mood and genre are all-or-nothing.** "Chill" and "relaxed" or "pop" and "indie pop" score the same as a total mismatch, so good near-matches can be ranked too low.
- **Energy dominates.** At 30 points, energy plus mood is over half of the score. A user whose taste is defined by something else, such as valence or acousticness, may get recommendations that feel off, and high-energy songs (metal, techno) can crowd out mellow ones for users with a mid-range energy target.
- **Closeness favors the middle.** Songs near the middle of a feature's range are never far from any target, so they can score decently for everyone, while extreme songs (such as classical or metal) only win for users with extreme targets.
- **One profile, one taste.** A single set of targets cannot represent someone who likes both calm study music and workout music, so one of the two will always be underserved.
- **Labels are subjective.** The mood and genre tags come from whoever labeled the CSV, and the system takes them as ground truth.
- **Rich-get-richer is absent, but so is diversity.** Nothing prevents the top results from being near-duplicates (for example, three lofi songs from the same artist).

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
============================================================
                    TOP RECOMMENDATIONS                     
============================================================

#1  Midnight Coding by LoRoom
    Score: 98.58
    Reasons:
      - mood match (+25.0)
      - genre match (+15.0)
      - energy closeness (+29.4)
      - valence closeness (+9.8)
      - acousticness closeness (+9.6)
      - danceability closeness (+4.9)
      - tempo closeness (+4.9)
------------------------------------------------------------

#2  Library Rain by Paper Lanterns
    Score: 96.65
    Reasons:
      - mood match (+25.0)
      - genre match (+15.0)
      - energy closeness (+28.5)
      - valence closeness (+9.8)
      - acousticness closeness (+8.9)
      - danceability closeness (+4.9)
      - tempo closeness (+4.6)
------------------------------------------------------------

#3  Spacewalk Thoughts by Orbit Bloom
    Score: 76.95
    Reasons:
      - mood match (+25.0)
      - energy closeness (+26.4)
      - valence closeness (+9.3)
      - acousticness closeness (+8.3)
      - danceability closeness (+4.1)
      - tempo closeness (+3.9)
------------------------------------------------------------

#4  Focus Flow by LoRoom
    Score: 74.59
    Reasons:
      - genre match (+15.0)
      - energy closeness (+30.0)
      - valence closeness (+9.9)
      - acousticness closeness (+9.7)
      - danceability closeness (+5.0)
      - tempo closeness (+5.0)
------------------------------------------------------------

#5  Dust Road Hymn by Hollow Pines
    Score: 55.99
    Reasons:
      - energy closeness (+27.6)
      - valence closeness (+9.6)
      - acousticness closeness (+9.9)
      - danceability closeness (+4.8)
      - tempo closeness (+4.1)
------------------------------------------------------------
```
## Recommendation Output Comparison

Top 5 results for each profile, from `python src/main.py`:

### Late-Night Study

```
============================================================
           TOP RECOMMENDATIONS: Late-Night Study            
============================================================

#1  Midnight Coding by LoRoom
    Score: 98.58
    Reasons:
      - mood match (+25.0)
      - genre match (+15.0)
      - energy closeness (+29.4)
      - valence closeness (+9.8)
      - acousticness closeness (+9.6)
      - danceability closeness (+4.9)
      - tempo closeness (+4.9)
------------------------------------------------------------

#2  Library Rain by Paper Lanterns
    Score: 96.65
    Reasons:
      - mood match (+25.0)
      - genre match (+15.0)
      - energy closeness (+28.5)
      - valence closeness (+9.8)
      - acousticness closeness (+8.9)
      - danceability closeness (+4.9)
      - tempo closeness (+4.6)
------------------------------------------------------------

#3  Spacewalk Thoughts by Orbit Bloom
    Score: 76.95
    Reasons:
      - mood match (+25.0)
      - energy closeness (+26.4)
      - valence closeness (+9.3)
      - acousticness closeness (+8.3)
      - danceability closeness (+4.1)
      - tempo closeness (+3.9)
------------------------------------------------------------

#4  Focus Flow by LoRoom
    Score: 74.59
    Reasons:
      - genre match (+15.0)
      - energy closeness (+30.0)
      - valence closeness (+9.9)
      - acousticness closeness (+9.7)
      - danceability closeness (+5.0)
      - tempo closeness (+5.0)
------------------------------------------------------------

#5  Dust Road Hymn by Hollow Pines
    Score: 55.99
    Reasons:
      - energy closeness (+27.6)
      - valence closeness (+9.6)
      - acousticness closeness (+9.9)
      - danceability closeness (+4.8)
      - tempo closeness (+4.1)
------------------------------------------------------------
```

### High-Energy Pop

```
============================================================
            TOP RECOMMENDATIONS: High-Energy Pop            
============================================================

#1  Sunrise City by Neon Echo
    Score: 95.85
    Reasons:
      - mood match (+25.0)
      - genre match (+15.0)
      - energy closeness (+27.6)
      - valence closeness (+9.9)
      - acousticness closeness (+9.2)
      - danceability closeness (+4.7)
      - tempo closeness (+4.5)
------------------------------------------------------------

#2  Rooftop Lights by Indigo Parade
    Score: 77.53
    Reasons:
      - mood match (+25.0)
      - energy closeness (+25.8)
      - valence closeness (+9.6)
      - acousticness closeness (+7.5)
      - danceability closeness (+4.8)
      - tempo closeness (+4.8)
------------------------------------------------------------

#3  Gym Hero by Max Pulse
    Score: 72.44
    Reasons:
      - genre match (+15.0)
      - energy closeness (+29.1)
      - valence closeness (+9.2)
      - acousticness closeness (+9.5)
      - danceability closeness (+4.8)
      - tempo closeness (+4.8)
------------------------------------------------------------

#4  Warehouse 4AM by Pulse Theory
    Score: 58.15
    Reasons:
      - energy closeness (+29.7)
      - valence closeness (+8.8)
      - acousticness closeness (+9.7)
      - danceability closeness (+5.0)
      - tempo closeness (+5.0)
------------------------------------------------------------

#5  Salsa en la Azotea by Los Faroles
    Score: 55.48
    Reasons:
      - energy closeness (+29.4)
      - valence closeness (+9.5)
      - acousticness closeness (+8.3)
      - danceability closeness (+4.7)
      - tempo closeness (+3.6)
------------------------------------------------------------
```

### Chill Lofi

```
============================================================
              TOP RECOMMENDATIONS: Chill Lofi               
============================================================

#1  Library Rain by Paper Lanterns
    Score: 97.15
    Reasons:
      - mood match (+25.0)
      - genre match (+15.0)
      - energy closeness (+28.5)
      - valence closeness (+9.5)
      - acousticness closeness (+9.4)
      - danceability closeness (+4.9)
      - tempo closeness (+4.9)
------------------------------------------------------------

#2  Midnight Coding by LoRoom
    Score: 94.82
    Reasons:
      - mood match (+25.0)
      - genre match (+15.0)
      - energy closeness (+26.4)
      - valence closeness (+9.9)
      - acousticness closeness (+9.1)
      - danceability closeness (+4.7)
      - tempo closeness (+4.8)
------------------------------------------------------------

#3  Spacewalk Thoughts by Orbit Bloom
    Score: 80.75
    Reasons:
      - mood match (+25.0)
      - energy closeness (+29.4)
      - valence closeness (+9.0)
      - acousticness closeness (+8.8)
      - danceability closeness (+4.3)
      - tempo closeness (+4.2)
------------------------------------------------------------

#4  Focus Flow by LoRoom
    Score: 70.81
    Reasons:
      - genre match (+15.0)
      - energy closeness (+27.0)
      - valence closeness (+9.6)
      - acousticness closeness (+9.8)
      - danceability closeness (+4.8)
      - tempo closeness (+4.7)
------------------------------------------------------------

#5  Pine Creek Porch by Wren & Willow
    Score: 56.75
    Reasons:
      - energy closeness (+30.0)
      - valence closeness (+8.9)
      - acousticness closeness (+8.7)
      - danceability closeness (+4.6)
      - tempo closeness (+4.6)
------------------------------------------------------------
```

### Deep Intense Rock

```
============================================================
           TOP RECOMMENDATIONS: Deep Intense Rock           
============================================================

#1  Storm Runner by Voltline
    Score: 96.65
    Reasons:
      - mood match (+25.0)
      - genre match (+15.0)
      - energy closeness (+29.7)
      - valence closeness (+8.7)
      - acousticness closeness (+9.8)
      - danceability closeness (+4.2)
      - tempo closeness (+4.2)
------------------------------------------------------------

#2  Gym Hero by Max Pulse
    Score: 77.96
    Reasons:
      - mood match (+25.0)
      - energy closeness (+29.7)
      - valence closeness (+5.8)
      - acousticness closeness (+9.7)
      - danceability closeness (+3.1)
      - tempo closeness (+4.7)
------------------------------------------------------------

#3  Iron Requiem by Black Lantern
    Score: 54.73
    Reasons:
      - energy closeness (+28.5)
      - valence closeness (+8.7)
      - acousticness closeness (+9.6)
      - danceability closeness (+4.5)
      - tempo closeness (+3.4)
------------------------------------------------------------

#4  Warehouse 4AM by Pulse Theory
    Score: 52.95
    Reasons:
      - energy closeness (+29.1)
      - valence closeness (+6.2)
      - acousticness closeness (+9.9)
      - danceability closeness (+3.3)
      - tempo closeness (+4.4)
------------------------------------------------------------

#5  Night Drive Loop by Neon Echo
    Score: 49.42
    Reasons:
      - energy closeness (+24.9)
      - valence closeness (+8.6)
      - acousticness closeness (+8.6)
      - danceability closeness (+3.9)
      - tempo closeness (+3.5)
------------------------------------------------------------
```


**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



