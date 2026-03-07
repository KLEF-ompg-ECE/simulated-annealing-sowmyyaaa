"""
sa_timetable.py  —  Simulated Annealing: Exam Timetable Scheduling
===================================================================
This program is COMPLETE and works as-is. DO NOT rewrite it.

Your task:
  1. Read the code and understand how it works
  2. Run the 3 experiments described in README.md
  3. Save the plots and fill in your observations in README.md

HOW TO RUN
----------
    python sa_timetable.py

PROBLEM
-------
Schedule 10 university exams into 5 time slots so that no student
has two exams at the same time. A clash = two exams in the same slot
for the same student. Goal: minimise total clashes to zero.
"""

import random
import math
import matplotlib.pyplot as plt
import os

# =============================================================================
# PROBLEM DATA
# =============================================================================

EXAMS = [
    "Mathematics",       # 0
    "Physics",           # 1
    "Chemistry",         # 2
    "English",           # 3
    "History",           # 4
    "Computer Science",  # 5
    "Economics",         # 6
    "Biology",           # 7
    "Statistics",        # 8
    "Geography",         # 9
]

NUM_EXAMS = len(EXAMS)
NUM_SLOTS = 5

STUDENTS = [
    [0,1,5],[0,2,6],[1,3,7],[2,4,8],[3,5,9],
    [0,4,7],[1,6,8],[2,5,9],[3,6,0],[4,7,1],
    [5,8,2],[6,9,3],[7,0,4],[8,1,5],[9,2,6],
    [0,3,8],[1,4,9],[2,7,5],[3,8,6],[4,9,7],
    [0,5,2],[1,6,3],[2,7,4],[3,8,0],[4,9,1],
    [5,0,6],[6,1,7],[7,2,8],[8,3,9],[9,4,0],
]


# =============================================================================
# OBJECTIVE FUNCTION — counts how many clashes exist
# ── EXPERIMENT 3: you will swap this function ─────────────────────────────────
# =============================================================================

# VERSION A — Simple clash count (default, used in Experiments 1 & 2)
def count_clashes_simple(timetable):
    """
    Count total clashes. Every clash counts equally as 1.
    This is the DEFAULT objective function.
    """
    clashes = 0
    for student_exams in STUDENTS:
        seen_slots = set()
        for exam in student_exams:
            slot = timetable[exam]
            if slot in seen_slots:
                clashes += 1
            seen_slots.add(slot)
    return clashes


# VERSION B — Weighted clash count (use this for Experiment 3)
def count_clashes_weighted(timetable):
    """
    EXPERIMENT 3 — Weighted objective function.

    Instead of counting every clash equally, this version penalises
    a student having ALL THREE exams in the same slot much more heavily:
        • 2 exams in same slot  → counts as 1
        • 3 exams in same slot  → counts as 5  (much worse!)

    This guides SA to fix the worst clashes first.
    """
    clashes = 0
    for student_exams in STUDENTS:
        slot_count = {}
        for exam in student_exams:
            s = timetable[exam]
            slot_count[s] = slot_count.get(s, 0) + 1
        for count in slot_count.values():
            if count == 2:
                clashes += 1
            elif count >= 3:
                clashes += 5   # heavy penalty for triple clash
    return clashes


# ── Active objective function — change this line for Experiment 3 ─────────────
count_clashes = count_clashes_simple   # ← Experiment 3: change to count_clashes_weighted


# =============================================================================
# NEIGHBOUR FUNCTION — creates a nearby solution
# =============================================================================

def generate_neighbor(timetable):
    """
    Create a neighbouring timetable by moving ONE exam to a different slot.
    """
    new_tt = timetable[:]
    exam   = random.randint(0, NUM_EXAMS - 1)
    current_slot = timetable[exam]
    new_slot = random.choice([s for s in range(NUM_SLOTS) if s != current_slot])
    new_tt[exam] = new_slot
    return new_tt


# =============================================================================
# SIMULATED ANNEALING
# =============================================================================

def run_sa(
    initial_temp   = 100.0,
    cooling_rate   = 0.995,   # ← EXPERIMENT 2: change this value
    min_temp       = 0.1,
    max_iterations = 5000,
    seed           = 42,
):
    """
    Run Simulated Annealing to minimise exam timetable clashes.

    KEY PARAMETERS
    --------------
    initial_temp : how "hot" SA starts — higher means more random exploration early on
    cooling_rate : how fast temperature drops each step
                   • close to 1.0  (e.g. 0.995) = slow cooling, thorough search
                   • further from 1 (e.g. 0.80)  = fast cooling, quick but shallow

    Returns
    -------
    best_timetable : list of slot assignments
    best_clashes   : int — clashes in the best solution found
    clash_log      : list — best clashes recorded at each iteration (for plotting)
    temp_log       : list — temperature at each iteration (for plotting)
    """
    random.seed(seed)

    # Start from a random timetable
    current    = [random.randint(0, NUM_SLOTS - 1) for _ in range(NUM_EXAMS)]
    current_c  = count_clashes(current)
    best       = current[:]
    best_c     = current_c

    T          = initial_temp
    clash_log  = []
    temp_log   = []

    for _ in range(max_iterations):
        if T < min_temp:
            break

        neighbour  = generate_neighbor(current)
        neighbour_c = count_clashes(neighbour)
        delta       = neighbour_c - current_c   # positive = worse

        # Always accept improvements; sometimes accept worse solutions
        if delta < 0 or random.random() < math.exp(-delta / T):
            current   = neighbour
            current_c = neighbour_c

        if current_c < best_c:
            best   = current[:]
            best_c = current_c

        clash_log.append(best_c)
        temp_log.append(T)
        T *= cooling_rate

        if best_c == 0:
            break   # perfect solution found — stop early

    return best, best_c, clash_log, temp_log


# =============================================================================
# OUTPUT HELPERS
# =============================================================================

def print_timetable(timetable):
    print("\n📅  Final Timetable")
    print("─" * 42)
    for slot in range(NUM_SLOTS):
        in_slot = [EXAMS[i] for i in range(NUM_EXAMS) if timetable[i] == slot]
        print(f"  Slot {slot+1}:  {', '.join(in_slot) if in_slot else '(empty)'}")
    print("─" * 42)
    print(f"  Total clashes : {count_clashes(timetable)}\n")


def save_plot(clash_log, temp_log, filename, title):
    os.makedirs("plots", exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    ax1.plot(clash_log, color="crimson", linewidth=1.5)
    ax1.set_ylabel("Best Clashes")
    ax1.set_title(f"SA Convergence — {title}")
    ax1.grid(True, alpha=0.3)
    ax2.plot(temp_log, color="steelblue", linewidth=1.5)
    ax2.set_ylabel("Temperature")
    ax2.set_xlabel("Iteration")
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"  Saved → {filename}")


# =============================================================================
# ── RUN YOUR EXPERIMENTS HERE ────────────────────────────────────────────────
# =============================================================================

if __name__ == "__main__":

    # ══════════════════════════════════════════════════════════════════════════
    # EXPERIMENT 1 — Baseline
    # Run as-is. Do NOT change any parameters here.
    # ══════════════════════════════════════════════════════════════════════════
    print("=" * 48)
    print("  EXPERIMENT 1 — Baseline")
    print("=" * 48)

    tt, clashes, clash_log, temp_log = run_sa(
        initial_temp=100.0, cooling_rate=0.995,
        min_temp=0.1, max_iterations=5000, seed=42
    )
    print_timetable(tt)
    print(f"  Iterations     : {len(clash_log)}")
    print(f"  Start clashes  : {clash_log[0]}")
    print(f"  Final clashes  : {clashes}")
    save_plot(clash_log, temp_log,
              "plots/experiment_1.png", "Baseline  cooling_rate=0.995")

    # ══════════════════════════════════════════════════════════════════════════
    # EXPERIMENT 2 — Effect of Cooling Rate
    # TODO: Copy this block THREE times below (for 0.80, 0.95, 0.995).
    #       Change cooling_rate each time and change the plot filename.
    #       Record results in README.md.
    # ══════════════════════════════════════════════════════════════════════════

    # --- Copy and edit below this line ---

    # tt2, clashes2, cl2, tl2 = run_sa(
    #     initial_temp=100.0, cooling_rate=0.80,    # ← change this
    #     min_temp=0.1, max_iterations=5000, seed=42
    # )
    # print_timetable(tt2)
    # print(f"  Final clashes : {clashes2}")
    # save_plot(cl2, tl2, "plots/experiment_2a.png", "cooling_rate=0.80")   # ← change filename

    # ══════════════════════════════════════════════════════════════════════════
    # EXPERIMENT 3 — Weighted Objective Function
    # TODO:
    #   1. Scroll up to the line:
    #          count_clashes = count_clashes_simple
    #      Change it to:
    #          count_clashes = count_clashes_weighted
    #   2. Uncomment and run the block below.
    #   3. Compare results with Experiment 1 and record in README.md.
    # ══════════════════════════════════════════════════════════════════════════

    # --- Uncomment below after swapping the objective function ---

    # tt3, clashes3, cl3, tl3 = run_sa(
    #     initial_temp=100.0, cooling_rate=0.995,
    #     min_temp=0.1, max_iterations=5000, seed=42
    # )
    # print_timetable(tt3)
    # print(f"  Final clashes (weighted score) : {clashes3}")
    # save_plot(cl3, tl3, "plots/experiment_3.png", "Weighted objective function")
