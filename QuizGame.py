from Quiz import Quiz
from state_store import STATE_PATH, load_state, quiz_from_dict, quiz_to_dict, save_state


class QuizGame:
    def __init__(self):
        self.state = load_state(STATE_PATH)
        self.quizzes: list[Quiz] = [quiz_from_dict(d) for d in self.state["quizzes"]]

    @staticmethod
    def _prompt_nonempty(prompt: str) -> str:
        while True:
            raw = input(prompt).strip()
            if raw == "":
                print("⚠️ 입력이 비어 있습니다. 다시 입력하세요.")
                continue
            return raw

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

        best_score = self.state.get("best_score")
        score_pct = int(round(100 * correct / total)) if total else 0
        is_best = best_score is None or score_pct > best_score
        if is_best:
            self.state["best_score"] = score_pct
            self.state["best_correct"] = correct
            self.state["best_total"] = total
            print("🎉 새로운 최고 점수입니다!")
            save_state(self.state, STATE_PATH)

    def _list_quizzes(self) -> None:
        if not self.quizzes:
            print("\n📋 등록된 퀴즈가 없습니다.")
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("----------------------------------------")
        for i, q in enumerate(self.quizzes, 1):
            print(f"[{i}] {q.question}")
        print("----------------------------------------")

    def _show_best_score(self) -> None:
        best_score = self.state.get("best_score")
        if best_score is None:
            print("\n🏆 아직 최고 점수가 없습니다. 먼저 퀴즈를 풀어보세요.")
            return
        bc = self.state.get("best_correct")
        bt = self.state.get("best_total")
        print(f"\n🏆 최고 점수: {best_score}점 ({bt}문제 중 {bc}문제 정답)")

    def run(self) -> None:
        while True:
            print("\n========================================")
            print("       🎯 나만의 퀴즈 게임 🎯")
            print("========================================")
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가 (준비중)")
            print("3. 퀴즈 목록")
            print("4. 점수 확인")
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
            elif choice == 3:
                self._list_quizzes()
            elif choice == 4:
                self._show_best_score()
            elif choice == 5:
                print("\n종료합니다.")
                break
            else:
                print("\n해당 기능은 아직 준비중입니다.")
