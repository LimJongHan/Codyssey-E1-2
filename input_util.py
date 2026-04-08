"""콘솔 입력 유틸리티.

과제의 '공통 입력/예외 처리 기준'을 한 곳에서 일관되게 적용하기 위한 모듈이다.
- 입력 앞뒤 공백 제거
- 빈 입력/비숫자/범위 밖 입력 시 안내 후 재입력

주의: Ctrl+C(KeyboardInterrupt), EOF(EOFError) 처리는 호출부(메인 루프)에서 처리한다.
"""

def prompt_nonempty(prompt: str) -> str:
    """빈 문자열이 아닌 한 줄을 받을 때까지 반복해서 입력받는다."""
    while True:
        raw = input(prompt).strip()
        if raw == "":
            print("⚠️ 입력이 비어 있습니다. 다시 입력하세요.")
            continue
        return raw


def prompt_int_in_range(prompt: str, min_v: int, max_v: int) -> int:
    """정수 입력을 `min_v`~`max_v` 범위로 제한해 받을 때까지 반복한다."""
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
