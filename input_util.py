def prompt_nonempty(prompt: str) -> str:
    while True:
        raw = input(prompt).strip()
        if raw == "":
            print("⚠️ 입력이 비어 있습니다. 다시 입력하세요.")
            continue
        return raw


def prompt_int_in_range(prompt: str, min_v: int, max_v: int) -> int:
    while True:
        raw = input(prompt).strip()
        if raw == "":
            print(f"⚠️ 입력이 비어 있습니다. {min_v}~{max_v} 사이의 숫자를 입력하세요.")
            continue
        try:
            value = int(raw)
        except ValueError:
            print(f"⚠️ 숫자로 입력하세요. ({min_v}~{max_v})")
            continue
        if value < min_v or value > max_v:
            print(f"⚠️ {min_v}~{max_v} 사이의 숫자를 입력하세요.")
            continue
        return value
