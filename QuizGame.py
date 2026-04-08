from Quiz import Quiz


class QuizGame:
    def __init__(self):
        self.quizzes: list[Quiz] = []

    def run(self) -> None:
        print("\n========================================")
        print("       🎯 나만의 퀴즈 게임 🎯")
        print("========================================")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("========================================")
        input("선택: ")
