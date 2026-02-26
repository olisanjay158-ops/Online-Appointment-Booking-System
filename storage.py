import json
from pathlib import Path
from typing import Any, Dict, List

DATA_FILE = Path(__file__).resolve().parent.parent / "mock" / "users.json"

def load_users() -> List[Dict[str, Any]]:
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))

def save_users(users: List[Dict[str, Any]]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(users, indent=2), encoding="utf-8")

def add_user(user: Dict[str, Any]) -> Dict[str, Any]:
    users = load_users()
    users.append(user)
    save_users(users)
    return user