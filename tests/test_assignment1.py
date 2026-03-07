"""
Autograding Tests — Assignment 1: SA Exam Timetable (2 experiments)
====================================================================
Section A — Code runs correctly         (25 pts)
Section B — Plot files exist            (25 pts)
Section C — README observations filled  (35 pts)
Section D — Code was modified           (15 pts)
                                  TOTAL  100 pts

Run locally:  python -m pytest tests/test_assignment1.py -v
"""

import subprocess, sys, os, re
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# =============================================================================
# SECTION A — Code runs correctly  (25 pts)
# =============================================================================

class TestCodeRuns:

    @pytest.fixture(autouse=True, scope="class")
    def run_program(self, tmp_path_factory):
        r = subprocess.run(
            [sys.executable, "sa_timetable.py"],
            cwd=ROOT, capture_output=True, text=True, timeout=120
        )
        TestCodeRuns._result = r

    def test_runs_without_error(self):
        """Program must exit with code 0."""
        assert self._result.returncode == 0, \
            f"Program crashed (exit {self._result.returncode}):\n{self._result.stderr[:400]}"

    def test_output_mentions_clashes(self):
        """Output must mention 'clashes'."""
        assert "clashes" in self._result.stdout.lower(), \
            "Word 'clashes' not found in output"

    def test_output_shows_slot_labels(self):
        """Output must print Slot labels."""
        assert "Slot" in self._result.stdout, \
            "'Slot' not found — is print_timetable() called?"

    def test_output_shows_iterations(self):
        """Output must print iteration count."""
        assert "teration" in self._result.stdout, \
            "Iteration count not printed"

    def test_multiple_experiment_runs(self):
        """Output must show at least 2 runs (Exp 1 + at least one Exp 2 variant)."""
        count = self._result.stdout.count("Final clashes")
        assert count >= 2, \
            f"Expected ≥2 runs in output, found {count}"


# =============================================================================
# SECTION B — Plot files exist  (25 pts)
# =============================================================================

class TestPlotsExist:

    def _plot(self, fname):
        return os.path.join(ROOT, "plots", fname)

    def test_plots_directory_exists(self):
        assert os.path.isdir(os.path.join(ROOT, "plots")), \
            "plots/ directory not found"

    def test_experiment_1_exists(self):
        assert os.path.isfile(self._plot("experiment_1.png")), \
            "plots/experiment_1.png missing"

    def test_experiment_2a_exists(self):
        assert os.path.isfile(self._plot("experiment_2a.png")), \
            "plots/experiment_2a.png missing (cooling_rate=0.80)"

    def test_experiment_2b_exists(self):
        assert os.path.isfile(self._plot("experiment_2b.png")), \
            "plots/experiment_2b.png missing (cooling_rate=0.95)"

    def test_experiment_2c_exists(self):
        assert os.path.isfile(self._plot("experiment_2c.png")), \
            "plots/experiment_2c.png missing (cooling_rate=0.995)"

    def test_all_plots_non_empty(self):
        plots_dir = os.path.join(ROOT, "plots")
        if not os.path.isdir(plots_dir):
            pytest.skip("plots/ directory missing")
        for fname in ["experiment_1.png","experiment_2a.png",
                      "experiment_2b.png","experiment_2c.png"]:
            path = os.path.join(plots_dir, fname)
            if os.path.isfile(path):
                assert os.path.getsize(path) > 1000, \
                    f"{fname} appears empty — was it saved correctly?"


# =============================================================================
# SECTION C — README observations filled in  (35 pts)
# =============================================================================

class TestREADME:

    @pytest.fixture(autouse=True)
    def load_readme(self):
        path = os.path.join(ROOT, "README.md")
        assert os.path.isfile(path), "README.md not found"
        self.text = open(path).read()

    PLACEHOLDERS = ["YOUR ANSWER", "YOUR OBSERVATION", "YOUR REFLECTION", "PASTE"]

    def _filled(self, marker):
        m = re.search(
            rf"{re.escape(marker)}.*?```\n(.*?)```", self.text, re.DOTALL)
        if not m:
            return False
        content = m.group(1).strip()
        return bool(content) and not any(p in content for p in self.PLACEHOLDERS)

    def test_student_name_filled(self):
        line = self.text.split("Student Name")[1].split("\n")[0]
        assert "___" not in line, "Student name is still blank"

    def test_q1_answered(self):
        assert self._filled("Q1."), \
            "Q1 still placeholder — answer what count_clashes() measures"

    def test_q2_answered(self):
        assert self._filled("Q2."), \
            "Q2 still placeholder — answer what generate_neighbor() does"

    def test_q3_answered(self):
        assert self._filled("Q3."), \
            "Q3 still placeholder — explain the acceptance probability line"

    def test_exp1_timetable_pasted(self):
        assert self._filled("Copy the printed timetable"), \
            "Experiment 1 timetable not pasted"

    def test_exp1_observation_written(self):
        assert self._filled("Look at `plots/experiment_1.png`"), \
            "Experiment 1 plot observation still blank"

    def test_exp2_results_table_filled(self):
        section = self.text[
            self.text.find("Experiment 2"):self.text.find("## Summary")]
        rows = [l for l in section.split("\n") if l.startswith("| 0.")]
        filled = [r for r in rows
                  if r.count("|") >= 4 and
                  any(c.strip() not in ("", "Yes", "No", " ")
                      for c in r.split("|")[2:5])]
        assert len(filled) >= 2, \
            f"Experiment 2 table: only {len(filled)} rows have data (need ≥ 2)"

    def test_exp2_observation_written(self):
        assert self._filled("Compare the three plots"), \
            "Experiment 2 observation (compare plots) still blank"

    def test_exp2_best_rate_answered(self):
        assert self._filled("Which cooling_rate gave the best result"), \
            "Experiment 2 'Which cooling_rate gave best result?' not answered"

    def test_reflection_written(self):
        assert self._filled("most important thing you learned about Simulated"), \
            "Summary reflection still blank"


# =============================================================================
# SECTION D — Code was modified  (15 pts)
# =============================================================================

class TestCodeModified:

    @pytest.fixture(autouse=True)
    def load_code(self):
        self.code = open(os.path.join(ROOT, "sa_timetable.py")).read()

    def test_exp2_rate_080_present(self):
        assert "0.80" in self.code or "0.8," in self.code or \
               "cooling_rate = 0.8\n" in self.code, \
            "cooling_rate=0.80 not found in code — add Experiment 2a block"

    def test_exp2_rate_095_present(self):
        assert "0.95" in self.code, \
            "cooling_rate=0.95 not found in code — add Experiment 2b block"

    def test_exp2_three_plot_saves(self):
        count = self.code.count("experiment_2")
        assert count >= 3, \
            f"Expected 3 experiment_2 plot saves in code, found {count}"
