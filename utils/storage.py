
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
PROFILES = DATA_DIR / "profiles.json"
BOARDS = DATA_DIR / "boards.json"

def _read(path):
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return {}

def _write(path, data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ---- Profiles ----
def list_profiles():
    return list(_read(PROFILES).keys())

def get_profile(name: str):
    return _read(PROFILES).get(name)

def save_profile(name: str, profile: dict):
    data = _read(PROFILES)
    data[name] = profile
    _write(PROFILES, data)

def delete_profile(name: str):
    data = _read(PROFILES)
    if name in data:
        data.pop(name)
        _write(PROFILES, data)

# ---- Boards / Tracking ----
def get_board(name: str):
    return _read(BOARDS).get(name, {"saved": [], "tracked": {}})

def save_board(name: str, board: dict):
    data = _read(BOARDS)
    data[name] = board
    _write(BOARDS, data)
