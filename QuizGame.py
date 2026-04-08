from Quiz import Quiz


class QuizGame:
    def __init__(self):
        self.quizzes: list[Quiz] = self._default_quizzes()

    @staticmethod
    def _default_quizzes() -> list[Quiz]:
        # 과제 요구: 선택 주제(기초 산수) 기본 퀴즈 5개 이상
        return [
            Quiz("2 + 3 = ?", ["4", "5", "6", "7"], 2),
            Quiz("10 - 4 = ?", ["4", "5", "6", "7"], 3),
            Quiz("3 * 4 = ?", ["10", "11", "12", "13"], 3),
            Quiz("12 / 3 = ?", ["2", "3", "4", "6"], 3),
            Quiz("9 + 7 = ?", ["14", "15", "16", "17"], 3),
        ]

    @staticmethod
    def _prompt_menu() -> int:
        while True:
            raw = input("선택: ").strip()
            if raw == "":
                print("⚠️ 입력이 비어 있습니다. 1~5 중 하나를 입력하세요.")
                continue
            try:
                value = int(raw)
            except ValueError:
                print("⚠️ 숫자로 입력하세요. (1~5)")
                continue
            if value < 1 or value > 5:
                print("⚠️ 1~5 사이의 숫자를 입력하세요.")
                continue
            return value

    @staticmethod
    def _prompt_answer() -> int:
        while True:
            raw = input("정답 입력 (1~4): ").strip()
            if raw == "":
                print("⚠️ 입력이 비어 있습니다. 1~4 중 하나를 입력하세요.")
                continue
            try:
                value = int(raw)
            except ValueError:
                print("⚠️ 숫자로 입력하세요. (1~4)")
                continue
            if value < 1 or value > 4:
                print("⚠️ 1~4 사이의 숫자를 입력하세요.")
                continue
            return value

    def _play_quiz(self) -> None:
        if not self.quizzes:
            print("\n저장된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        total = len(self.quizzes)
        correct = 0
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")

        for idx, quiz in enumerate(self.quizzes, 1):
            print("\n----------------------------------------")
            quiz.display(idx)
            user_answer = self._prompt_answer()
            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!")
                correct += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        print("\n========================================")
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답!")
        print("========================================")

    def run(self) -> None:
        while True:
            print("\n========================================")
            print("       🎯 나만의 퀴즈 게임 🎯")
            print("========================================")
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가 (준비중)")
            print("3. 퀴즈 목록 (준비중)")
            print("4. 점수 확인 (준비중)")
            print("5. 종료")
            print("========================================")

            try:
                choice = self._prompt_menu()
            except (KeyboardInterrupt, EOFError):
                print("\n\n입력이 중단되었습니다. 종료합니다.")
                break

            if choice == 1:
                try:
                    self._play_quiz()
                except (KeyboardInterrupt, EOFError):
                    print("\n\n입력이 중단되었습니다. 메뉴로 돌아갑니다.")
            elif choice == 5:
                print("\n종료합니다.")
                break
            else:
                print("\n해당 기능은 아직 준비중입니다.")
