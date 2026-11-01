# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **Selecta 1.0**  

**Answer:**

**Selecta 1.0**. It matches songs to the vibe a listener asks for.

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

**Answer:**

**Goal.** Selecta suggests the top 5 songs from a small catalog for one listener. It ranks songs by how close they are to what the listener says they want.

**Assumptions about the user.** The listener knows their favorite genre and mood. They can pick target levels for energy, valence, acousticness, danceability and tempo. They have one taste at a time e.g Late Night Study.

**Intended use.** This is a classroom project. It is for learning how a simple recommender works. 

**Not intended for.**

- Real music apps or real users. The catalog is only 20 songs.
- Judging a person's taste or making decisions about them.
- Replacing a system that learns from listening history.
- Listeners whose taste is not in the catalog, like K-pop or gospel.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

**Answer:**

Think of the recommender as a judge giving every song in the catalog a grade out of 100 based on how well it fits one listener, then handing back the songs with the best grades.

**What it looks at.** For each song it considers its genre, its mood, and five "feel" measures: energy (calm vs. intense), valence (sad vs. happy sounding), acousticness (electronic vs. natural instruments), danceability, and tempo (how fast it is).

**What the listener tells it.** The listener names a favorite genre and a favorite mood, and picks a target level for each of the feel measures, such as "I want high energy, fairly happy, not very acoustic."

**How the grade is built.** Each feature is worth a certain number of points, and the points add up to 100:

- Energy is the most important, worth up to about 49 points.
- Mood is worth about 20 points, and genre is worth about 6.
- Valence and acousticness are worth up to about 8 points each.
- Danceability and tempo are worth up to about 4 points each.

(These are the weights after my weight-shift experiment. I doubled energy and halved genre, then rescaled so the total is still 100.)

Genre and mood are all-or-nothing: a song gets the full points if it matches the listener's favorite exactly, and zero otherwise. The feel measures work like a "closeness" test. A song that lands right on the listener's target gets the full points, and the further away it is, the fewer points it earns. So a song with slightly too much energy still scores well, while one that is the opposite of what they want earns almost nothing for that feature.

**Picking the winners.** Once every song has a grade, they are sorted from highest to lowest. If two songs tie, the one whose energy is closer to what the listener wants goes first, and if they are still tied, they are put in alphabetical order by title. The top few songs are returned, each with a short note explaining where its points came from (for example, "mood match" or "energy closeness").

**What changed from the starter.** The starter code only had empty placeholders and returned nothing. I added the code that reads the song file, the point system described above, and the sorting step that produces the final ranked list with explanations.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

**Answer:**

The catalog is `data/songs.csv`. It has 20 songs. Each song has a title, artist, genre, mood, and five numbers: energy, tempo, valence, danceability and acousticness.

There are 17 genres and 16 moods. Lofi has 3 songs and pop has 2. Every other genre has just 1 song. Chill has 3 songs, happy and intense have 2 each, and every other mood has 1.

I did not add or remove any songs. Some taste is missing. There is no K-pop, gospel, or most world music. There are no lyrics, no language, no song year and no popularity. The catalog is too small to cover most real tastes.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

**Answer:**

It works best for listeners at the clear ends of the energy scale. The Late-Night Study, Chill Lofi and High-Energy Pop profiles all got top songs that matched my gut feeling. For example, Chill Lofi got Library Rain and Midnight Coding first.

Different listeners got very different lists. Pop, Rock and the two lofi profiles shared almost no songs across the quiet and loud groups. The reasons are easy to read, so I can see why each song ranked where it did.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

**Answer:**

The biggest weakness I found is that, after the weight-shift experiment, energy is worth about half of the total score (roughly 49 of 100 points), so it can drown out what a listener says they want in mood or genre. A mood match is worth only about 20 points, which is the same as an energy gap of about 0.4, and every "chill" song in the catalog has energy of 0.42 or lower. A listener who asks for a chill mood but sets a high energy target will therefore get high-energy pop or techno ahead of any chill song, and the genre bonus (about 6 points) is too small to change that. The mood and genre checks also require an exact text match, so "relaxed" earns nothing from a "chill" or "peaceful" song. Because most genres and moods appear on just one song in a 20-song catalog, many listeners can only match one song on those features, while the three lofi/chill songs mean lofi fans get a top five of near-identical tracks.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

**Answer:**

**Profiles tested.** I ran four profiles from `src/main.py` with the top 5 results for each: Late-Night Study (lofi, chill, energy 0.40), High-Energy Pop (pop, happy, energy 0.90), Chill Lofi (lofi, chill, energy 0.30), and Deep Intense Rock (rock, intense, energy 0.92, dark valence 0.35). I looked for whether the top songs matched my intuition for each listener and whether different listeners got meaningfully different lists. The top 5 for each were:

| Profile | #1 | #2 | #3 | #4 | #5 |
|---|---|---|---|---|---|
| Late-Night Study | Midnight Coding | Library Rain | Spacewalk Thoughts | Focus Flow | Coffee Shop Stories |
| High-Energy Pop | Sunrise City | Rooftop Lights | Gym Hero | Warehouse 4AM | Salsa en la Azotea |
| Chill Lofi | Library Rain | Midnight Coding | Spacewalk Thoughts | Focus Flow | Pine Creek Porch |
| Deep Intense Rock | Storm Runner | Gym Hero | Iron Requiem | Warehouse 4AM | Salsa en la Azotea |

**Pairwise comparisons.**

- **Late-Night Study vs. High-Energy Pop:** The lists have no songs in common. Study wants energy 0.40 and acoustic textures (acousticness 0.75), so it gets quiet lofi, ambient and jazz. Pop wants energy 0.90 and polished electronic sound (acousticness 0.10), so it gets pop, techno and latin. This makes sense because the two profiles sit at opposite ends of both energy and acousticness.
- **Late-Night Study vs. Chill Lofi:** These are nearly the same list (four of five songs match), and only the order changes. Study targets energy 0.40, so Midnight Coding (0.42) wins. Chill Lofi targets 0.30, so Library Rain (0.35) wins and Spacewalk Thoughts (0.28) climbs from 84 to 90 points. The fifth slot swaps Coffee Shop Stories (0.37) for Pine Creek Porch (0.30), which is the song closest to the lower energy target. The small 0.10 energy difference reshuffles the ranking as expected, but it also shows that two similar listeners get almost no variety.
- **Late-Night Study vs. Deep Intense Rock:** The lists have no songs in common. Rock wants loud, dark, non-acoustic songs (energy 0.92, acousticness 0.08), the opposite of Study's profile, so nothing from the lofi cluster appears.
- **High-Energy Pop vs. Chill Lofi:** The lists have no songs in common. Pop and Chill Lofi differ by 0.60 in target energy and 0.70 in target acousticness, and neither shares a genre or mood label. This is the clearest example of the model separating two very different listeners.
- **High-Energy Pop vs. Deep Intense Rock:** These two share three songs (Gym Hero, Warehouse 4AM and Salsa en la Azotea), because both want energy around 0.90. The differences come from the categorical bonuses. Pop's #1 and #2 are the happy songs (Sunrise City, Rooftop Lights), while Rock's #1 is Storm Runner, the only rock song. Gym Hero moves from #3 for Pop (genre match) to #2 for Rock (it matches the "intense" mood). Rock's low valence target also pushes the bright pop songs out of its list.
- **Chill Lofi vs. Deep Intense Rock:** These lists have no songs in common, because the profiles are on opposite ends of energy, valence and acousticness. Neither profile's list contains a song at the other's end of the energy scale.

**What surprised me.**

- Gym Hero (pop, intense, 0.93 energy) ranked #2 for the rock listener, ahead of Iron Requiem, the metal song I would have expected. It scored well because it matches "intense" and its energy is close, even though it is a polished pop song. Iron Requiem only got #3 because it has no genre or mood match and its tempo scales to 1.17, above the 0-1 range.
- Salsa en la Azotea (happy, valence 0.90) made the rock listener's top 5 even though that listener wanted a dark valence of 0.35. Energy closeness outweighed the mismatch on valence, which supports the limitation in Section 6.
- After the #1 song, the scores for the non-lofi profiles drop quickly (about 97 to 88 for Rock, 95 to 84 for Pop). That is because each of those profiles has only one song matching its genre. The lofi profiles stay above 84 for three songs because the catalog has three lofi songs.
- I only tested profiles at the extremes of energy. A mid-energy listener (around 0.65) falls into the gap between 0.58 and 0.75 in the catalog, so I would expect weaker results for them, but I have not tested that yet.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

**Answer:**

1. **Lower the energy weight.** Energy is about half of the score. I would cut it to about 30 points. Then mood and genre could change the ranking more.
2. **Match similar moods.** Give partial credit for close moods, like chill, relaxed and peaceful. Right now only an exact match counts.
3. **Add variety.** Limit the top 5 to two songs per genre or artist. Lofi fans would see more than near-identical songs.
4. **Fix the tempo scale.** Compute it from the catalog instead of fixed numbers, so very fast songs like Iron Requiem are not penalized.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

**Answer:**

I learned that a few weights can decide almost everything. When I made energy count more, it started to beat the mood and genre the listener asked for. Small choices in the scoring have big effects.

The most surprising result was Gym Hero, a pop song, ranking second for the rock listener. It matched the "intense" mood and had close energy. That showed me that the label a song has can matter more than what the song sounds like.

Now I think of a music app as a set of choices made by people. If a catalog is small or skewed, some listeners will get worse results, and the app may never show them anything new.
