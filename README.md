# Assignment 1 — Simulated Annealing: Exam Timetable Scheduling
## Observation Report

**Student Name  :** SOWMYA
**Student ID    :**2310040060
**Date Submitted:** 25/3/2026

---

## How to Submit

1. Run each experiment following the instructions below
2. Fill in every answer box — do not leave placeholders
3. Make sure the `plots/` folder contains all required images
4. Commit this README and the `plots/` folder to your GitHub repo

---

## Before You Begin — Read the Code

Open `sa_timetable.py` and read through it. Then answer these questions.

**Q1. What does `count_clashes()` measure? What value means a perfect timetable?**

```
[count_clashes() measures the total number of exam conflicts where a student has more than one exam scheduled in the same time slot. It checks all students and counts such overlaps. A value of 0 means a perfect timetable with no clashes. ]
```

**Q2. What does `generate_neighbor()` do? How is the new timetable different from the current one?**

```
[generate_neighbor() creates a new timetable by randomly selecting one exam and assigning it to a different time slot. The new timetable differs from the current one by only one small change. This helps in exploring nearby solutions gradually.]
```

**Q3. In `run_sa()`, there is this line:**
```python
if delta < 0 or random.random() < math.exp(-delta / T):
```
**What does this line decide? Why does SA sometimes accept a worse solution?**

```
[ This line decides whether to accept the new solution. If the new solution is better (delta < 0), it is always accepted; if it is worse, it may still be accepted based on probability. This allows Simulated Annealing to escape local minima and explore better solutions.]
```

---

## Experiment 1 — Baseline Run

**Instructions:** Run the program without changing anything.
```bash
python sa_timetable.py
```

**Fill in this table:**

| Metric | Your result |
|--------|-------------|
| Number of iterations completed | 1379 |
| Clashes at iteration 1 | 12 |
| Final best clashes | 3 |
| Did SA reach 0 clashes? (Yes / No) | No |

**Copy the printed timetable output here:**
```
Final Timetable
------------------------------------------
Slot 1: Geography
Slot 2: Chemistry, English
Slot 3: History, Computer Science, Economics
Slot 4: Biology, Statistics
Slot 5: Mathematics, Physics
------------------------------------------
Total clashes : 3
```

**Look at `plots/experiment_1.png` and describe what you see (2–3 sentences).**  
*Where does the biggest drop in clashes happen? Does the curve flatten out?*
```
[ The biggest drop in clashes happens in the early iterations when the temperature is high, dropping quickly from around 12 to 6. After that, the improvement becomes gradual and the curve starts to flatten. Towards the end, the curve stabilizes at around 3 clashes, showing convergence without reaching zero. ]
```

---

## Experiment 2 — Effect of Cooling Rate

**Instructions:** In `sa_timetable.py`, find the `# EXPERIMENT 2` block in `__main__`.  
Copy it three times and run with `cooling_rate` = **0.80**, **0.95**, and **0.995**.  
Save plots as `experiment_2a.png`, `experiment_2b.png`, `experiment_2c.png`.

**Results table:**
| cooling_rate | Final clashes | Iterations completed | Reached 0 clashes? |
|-------------|---------------|----------------------|--------------------|
| 0.80        | 8             | 31                   | No                 |
| 0.95        | 3             | 135                  | No                 |
| 0.995       | 3             | 1379                 | No                 |

**Compare the three plots. What do you notice about how fast vs slow cooling affects the result? (3–4 sentences)**  
*Hint: Fast cooling = temperature drops quickly. Does it have time to explore well?*
```
[Fast cooling (0.80) causes the temperature to drop very quickly, resulting in very few iterations and poor exploration of the solution space, which leads to higher clashes. Moderate cooling (0.95) allows more iterations and better improvement, reducing clashes more effectively. Slow cooling (0.995) provides the most gradual decrease in temperature, allowing thorough exploration and steady improvement. As a result, slower cooling produces better and more stable solutions. ]
```

**Which cooling_rate gave the best result? Why do you think that is?**
```
[The best result is obtained with cooling_rate = 0.995 because it allows the algorithm to explore more solutions due to slower cooling. This helps avoid local minima and leads to a better final timetable with fewer clashes. ]
```

---

## Summary

**Complete this table with your best result from each experiment:**

| Experiment | Key setting | Final clashes | Main finding in one sentence |
|------------|-------------|---------------|------------------------------|
| 1 — Baseline | cooling_rate = 0.995 | 3 | SA improves the solution but may not reach the optimal result every time. |
| 2 — Cooling rate | cooling_rate = 0.995 | 3 | Slower cooling leads to better exploration and improved solution quality. |

**In your own words — what is the most important thing you learned about Simulated Annealing from these experiments? (3–5 sentences)**
```
[ The most important thing I learned is that Simulated Annealing depends heavily on the cooling schedule. A high temperature allows the algorithm to explore many solutions, even accepting worse ones to escape local minima. If the cooling is too fast, the algorithm converges quickly but may get stuck in a poor solution. Slower cooling allows better exploration and improves the chances of finding a good solution. Therefore, choosing the right cooling rate is crucial for achieving optimal results. ]
```

---

## Submission Checklist

- [x] Student name and ID filled in
- [x] Q1, Q2, Q3 answered
- [x] Experiment 1: table filled, timetable pasted, plot observation written
- [x] Experiment 2: results table filled (3 rows), observation and answer written
- [x] Summary table completed and reflection written
- [x] `plots/` contains: `experiment_1.png`, `experiment_2a.png`, `experiment_2b.png`, `experiment_2c.png`
