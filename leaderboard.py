import json
import os
import time
from typing import List, Dict

FILE_PATH = "leaderboard.json"
MAX_ENTRIES = 10


def _atomic_write(path: str, data: str):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(data)
    os.replace(tmp, path)


def load() -> List[Dict]:
    if not os.path.exists(FILE_PATH):
        return []
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception:
        # corrupted file: ignore and return empty leaderboard
        return []
    return []


def save(entries: List[Dict]):
    # ensure entries is serializable
    text = json.dumps(entries, ensure_ascii=False, indent=2)
    _atomic_write(FILE_PATH, text)


def add_score(name: str, score: int):
    name = (name or "Player")[:20]
    entries = load()
    entries.append({"name": name, "score": int(score), "ts": int(time.time())})
    entries.sort(key=lambda e: e["score"], reverse=True)
    entries = entries[:MAX_ENTRIES]
    save(entries)


def get_top(n: int = 10) -> List[Dict]:
    return load()[:n]
