"""프로그램 진입점.

과제 요구사항에 따라 전체 흐름(메뉴/게임 진행/저장)은 `QuizGame`이 담당하고,
이 파일은 실행만 담당한다.
"""

from QuizGame import QuizGame


if __name__ == "__main__":
    QuizGame().run()
