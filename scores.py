import json, os

SCORES_FILE = os.path.join(os.path.dirname(__file__), "highscores.json")
GAMES = ["Pac-Man", "Galaga", "Donkey Kong", "Street Fighter II"]

def load_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'r') as f:
            return json.load(f)
    return {g: [] for g in GAMES}

def save_score(game, name, score):
    scores = load_scores()
    scores.setdefault(game, []).append({"name": name, "score": score})
    scores[game] = sorted(scores[game], key=lambda x: x["score"], reverse=True)[:10]
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f, indent=2)

def get_all_scores():
    return load_scores()
