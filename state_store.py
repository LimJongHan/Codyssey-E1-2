import json
from pathlib import Path

from Quiz import Quiz

ROOT = Path(__file__).resolve().parent
STATE_PATH = ROOT / "state.json"
SCHEMA_VERSION = 1


def quiz_to_dict(q: Quiz) -> dict:
    return {
        "question": q.question,
        "choices": q.choices,
        "answer": q.answer,
        "hint": q.hint,
    }


def quiz_from_dict(d: dict) -> Quiz:
    return Quiz(
        d["question"],
        list(d["choices"]),
        int(d["answer"]),
        d.get("hint"),
    )


def default_quizzes() -> list[Quiz]:
    return [
        Quiz("2 + 3 = ?", ["4", "5", "6", "7"], 2, hint="2에 3을 더합니다."),
        Quiz("10 - 4 = ?", ["4", "5", "6", "7"], 3, hint="10에서 4를 뺍니다."),
        Quiz("3 * 4 = ?", ["10", "11", "12", "13"], 3, hint="3을 4번 더합니다."),
        Quiz("12 / 3 = ?", ["2", "3", "4", "6"], 3, hint="12를 3등분합니다."),
        Quiz("9 + 7 = ?", ["14", "15", "16", "17"], 3, hint="한 자리 수 덧셈입니다."),
    ]


def default_state() -> dict:
    return {
        "version": SCHEMA_VERSION,
        "quizzes": [quiz_to_dict(q) for q in default_quizzes()],
        "best_score": None,
        "best_correct": None,
        "best_total": None,
        "history": [],
    }


def _is_valid_quiz_dict(d: dict) -> bool:
    if not isinstance(d, dict):
        return False
    if not isinstance(d.get("question"), str) or d["question"].strip() == "":
        return False
    choices = d.get("choices")
    if not isinstance(choices, list) or len(choices) != 4:
        return False
    if not all(isinstance(c, str) and c.strip() != "" for c in choices):
        return False
    try:
        answer = int(d.get("answer"))
    except (TypeError, ValueError):
        return False
    if answer < 1 or answer > 4:
        return False
    hint = d.get("hint")
    if hint is not None and not isinstance(hint, str):
        return False
    return True


def _sanitize_state(data: dict) -> tuple[dict, bool]:
    """
    state.json 구조가 일부 깨져도 프로그램이 실행되도록 보정한다.
    - quizzes: 유효한 항목만 남기고, 전부 무효면 기본 퀴즈로 복구
    - best_* / history: 타입이 이상하면 기본값으로 보정
    """
    changed = False

    if not isinstance(data, dict):
        return default_state(), True

    quizzes = data.get("quizzes")
    if not isinstance(quizzes, list):
        quizzes = []
        changed = True

    valid_quizzes = [q for q in quizzes if _is_valid_quiz_dict(q)]
    if len(valid_quizzes) != len(quizzes):
        changed = True
    if not valid_quizzes:
        valid_quizzes = [quiz_to_dict(q) for q in default_quizzes()]
        changed = True
    data["quizzes"] = valid_quizzes

    # best_score: int 또는 None
    bs = data.get("best_score")
    if bs is not None and not isinstance(bs, int):
        changed = True
        data["best_score"] = None
    # best_correct/best_total: int 또는 None
    for k in ("best_correct", "best_total"):
        v = data.get(k)
        if v is not None and not isinstance(v, int):
            changed = True
            data[k] = None

    hist = data.get("history")
    if not isinstance(hist, list):
        data["history"] = []
        changed = True

    data.setdefault("version", SCHEMA_VERSION)
    data.setdefault("best_score", None)
    data.setdefault("best_correct", None)
    data.setdefault("best_total", None)
    data.setdefault("history", [])
    return data, changed


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

    data, changed = _sanitize_state(data)
    if changed:
        print("⚠️ state.json 구조가 올바르지 않아 기본 규칙으로 복구/정리했습니다.")
        save_state(data, path)
    return data


def save_state(data: dict, path: Path = STATE_PATH) -> bool:
    try:
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except OSError as exc:
        print(f"⚠️ state.json 저장에 실패했습니다: {exc}")
        return False
