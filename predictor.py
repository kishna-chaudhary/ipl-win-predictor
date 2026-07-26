import math
import random
from functools import lru_cache

TEAMS = [
    "CSK",
    "DC",
    "GT",
    "KKR",
    "LSG",
    "MI",
    "PK",
    "RR",
    "RCB",
    "SRH",
]

CITIES = [
    "Ahmedabad",
    "Bengaluru",
    "Chennai",
    "Delhi",
    "Hyderabad",
    "Kolkata",
    "Mumbai",
    "Pune",
]

FEATURE_COLUMNS = ["batting_team", "bowling_team", "city", "current_runs", "overs_completed", "wickets", "target_runs"]


class SimpleLogisticRegression:
    def __init__(self):
        self.weights = {
            "batting_team": {team: 0.0 for team in TEAMS},
            "bowling_team": {team: 0.0 for team in TEAMS},
            "city": {city: 0.0 for city in CITIES},
            "current_runs": 0.01,
            "overs_completed": 0.04,
            "wickets": 0.14,
            "target_runs": -0.002,
            "runs_needed": -0.016,
            "remaining_overs": -0.16,
            "wickets_left": 0.19,
            "run_rate_needed": -0.16,
        }

    def fit(self, rows):
        return self

    def predict_proba(self, rows):
        results = []
        for row in rows:
            score = self._score(row)
            probability = 1 / (1 + math.exp(-score))
            results.append([1 - probability, probability])
        return results

    def _score(self, row):
        batting_team = row.get("batting_team", "CSK")
        bowling_team = row.get("bowling_team", "MI")
        city = row.get("city", "Chennai")
        current_runs = float(row.get("current_runs", 0))
        overs_completed = float(row.get("overs_completed", 0))
        wickets = float(row.get("wickets", 0))
        target_runs = float(row.get("target_runs", 0))

        runs_needed = max(target_runs - current_runs, 0.0)
        remaining_overs = max(20 - overs_completed, 0.1)
        wickets_left = max(10 - wickets, 0.0)
        run_rate_needed = runs_needed / remaining_overs if remaining_overs > 0 else 0.0

        score = (
            self.weights["current_runs"] * current_runs
            + self.weights["overs_completed"] * overs_completed
            + self.weights["wickets"] * wickets
            + self.weights["target_runs"] * target_runs
            + self.weights["runs_needed"] * runs_needed
            + self.weights["remaining_overs"] * remaining_overs
            + self.weights["wickets_left"] * wickets_left
            + self.weights["run_rate_needed"] * run_rate_needed
            + self.weights["batting_team"].get(batting_team, 0.0)
            + self.weights["bowling_team"].get(bowling_team, 0.0)
            + self.weights["city"].get(city, 0.0)
            - 2.4
        )
        return score


def _build_model():
    model = SimpleLogisticRegression()
    return model.fit([])


@lru_cache(maxsize=1)
def get_model():
    return _build_model()


def predict_win_probability(inputs: dict, model=None) -> float:
    if model is None:
        model = get_model()

    row = {name: inputs.get(name) for name in FEATURE_COLUMNS}
    probability = model.predict_proba([row])[0][1]
    return round(float(probability), 3)
