import json
from pathlib import Path

from Quiz import Quiz

ROOT = Path(__file__).resolve().parent
STATE_PATH = ROOT / "state.json"
SCHEMA_VERSION = 1


def quiz_to_dict(q: Quiz) -> dict:
    return {"question": q.question, "choices": q.choices, "answer": q.answer}


def quiz_from_dict(d: dict) -> Quiz:
    return Quiz(d["question"], list(d["choices"]), int(d["answer"]))


def default_quizzes() -> list[Quiz]:
    return [
        Quiz("2 + 3 = ?", ["4", "5", "6", "7"], 2),
        Quiz("10 - 4 = ?", ["4", "5", "6", "7"], 3),
        Quiz("3 * 4 = ?", ["10", "11", "12", "13"], 3),
        Quiz("12 / 3 = ?", ["2", "3", "4", "6"], 3),
        Quiz("9 + 7 = ?", ["14", "15", "16", "17"], 3),
    ]


def default_state() -> dict:
    return {
        "version": SCHEMA_VERSION,
        "quizzes": [quiz_to_dict(q) for q in default_quizzes()],
        "best_score": None,
        "best_correct": None,
        "best_total": None,
    }


def load_state(path: Path = STATE_PATH) -> dict:
    if (not path.exists()) or path.stat().st_size == 0:
        data = default_state()
        save_state(data, path)
        return data
    try:
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("⚠️ state.json이 손상되어 기본 데이터로 복구합니다.")
        data = default_state()
        save_state(data, path)
        return data
    except OSError as exc:
        print(f"⚠️ state.json을 읽을 수 없습니다: {exc}. 기본 데이터로 진행합니다.")
        return default_state()

    if not isinstance(data.get("quizzes"), list):
        data["quizzes"] = []
    data.setdefault("version", SCHEMA_VERSION)
    data.setdefault("best_score", None)
    data.setdefault("best_correct", None)
    data.setdefault("best_total", None)
    return data


def save_state(data: dict, path: Path = STATE_PATH) -> bool:
    try:
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except OSError as exc:
        print(f"⚠️ state.json 저장에 실패했습니다: {exc}")
        return False
