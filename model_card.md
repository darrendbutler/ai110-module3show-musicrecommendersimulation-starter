# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

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

- Energy is the most important, worth up to 30 points.
- Mood is worth 25 points, and genre is worth 15.
- Valence and acousticness are worth up to 10 points each.
- Danceability and tempo are worth up to 5 points each.

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

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
