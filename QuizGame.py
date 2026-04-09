"""게임 전체(메뉴/출제/추가/삭제/점수/기록)를 관리하는 컨트롤러.

설계 요약:
- `Quiz`: 문항 모델(출력/정답 판정)
- `state_store`: state.json 저장/로드 + 스키마 복구
- `input_util`: 공통 입력 검증(빈 입력/비숫자/범위 밖 재입력)

점수 정책(보너스):
- 힌트를 사용하지 않고 정답: 1.0점
- 힌트를 한 번이라도 본 뒤 정답: 0.8점 (80점)
- 최종 점수는 (points / 총문항수) * 100 을 반올림한 백분율로 표시
"""

from Quiz import Quiz
from input_util import prompt_int_in_range, prompt_nonempty
from state_store import STATE_PATH, load_state, quiz_from_dict, quiz_to_dict, save_state
import random
from datetime import datetime, timezone


class QuizGame:
    def __init__(self):
        """state.json을 로드하고 퀴즈 목록을 메모리에 구성한다."""
        self.state = load_state(STATE_PATH)
        self.quizzes: list[Quiz] = [quiz_from_dict(d) for d in self.state["quizzes"]]

    @staticmethod
    def _prompt_menu() -> int:
        """메뉴 선택(1~7). 잘못된 입력은 재입력."""
        return prompt_int_in_range("선택: ", 1, 7)

    @staticmethod
    def _prompt_answer() -> int:
        """정답 번호 입력(1~4). 잘못된 입력은 재입력."""
        return prompt_int_in_range("정답 입력 (1~4): ", 1, 4)

    @staticmethod
    def _prompt_answer_or_hint() -> str:
        """정답(1~4) 또는 힌트 요청(h)을 입력받는다."""
        while True:
            raw = input("정답 입력 (1~4) / 힌트(h): ").strip().lower()
            if raw == "":
                print("⚠️ 입력이 비어 있습니다. 1~4 또는 h를 입력하세요.")
                continue
            if raw == "h":
                return "h"
            try:
                value = int(raw)
            except ValueError:
                print("⚠️ 1~4 또는 h로 입력하세요.")
                continue
            if value < 1 or value > 4:
                print("⚠️ 1~4 사이의 숫자를 입력하세요.")
                continue
            return str(value)

    def _play_quiz(self) -> None:
        """랜덤 출제 + 문제 수 선택 + 힌트/점수/히스토리 기록을 포함한 플레이 루틴."""
        if not self.quizzes:
            print("\n저장된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        total_available = len(self.quizzes)
        count = prompt_int_in_range(
            f"\n몇 문제를 풀까요? (1~{total_available}): ", 1, total_available
        )
        quizzes = list(self.quizzes)
        random.shuffle(quizzes)
        quizzes = quizzes[:count]

        total = len(quizzes)
        correct = 0
        hint_used = 0
        points = 0.0
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")

        for idx, quiz in enumerate(quizzes, 1):
            print("\n----------------------------------------")
            quiz.display(idx)
            used_hint_this = False
            while True:
                ans = self._prompt_answer_or_hint()
                if ans == "h":
                    if used_hint_this:
                        print("ℹ️ 이미 이 문제에서 힌트를 사용했습니다.")
                        continue
                    if quiz.hint:
                        print(f"💡 힌트: {quiz.hint}")
                    else:
                        print("💡 힌트가 없습니다.")
                    used_hint_this = True
                    hint_used += 1
                    continue
                user_answer = int(ans)
                break

            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!")
                correct += 1
                points += 0.8 if used_hint_this else 1.0
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        score_pct = int(round(100 * points / total)) if total else 0
        print("\n========================================")
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score_pct}점)")
        if hint_used:
            print(f"💡 힌트 사용: {hint_used}회 (힌트 사용 시 정답 0.8점 처리)")
        print("========================================")

        best_score = self.state.get("best_score")
        is_best = best_score is None or score_pct > best_score
        if is_best:
            self.state["best_score"] = score_pct
            self.state["best_correct"] = correct
            self.state["best_total"] = total
            print("🎉 새로운 최고 점수입니다!")
            save_state(self.state, STATE_PATH)

        # 기록 히스토리 저장(보너스): 최고 점수와 별개로 매 플레이 기록을 누적 저장한다.
        ts = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
        self.state.setdefault("history", [])
        self.state["history"].append(
            {
                "timestamp": ts,
                "total": total,
                "correct": correct,
                "points": points,
                "score_pct": score_pct,
                "hint_used": hint_used,
            }
        )
        save_state(self.state, STATE_PATH)

    def _list_quizzes(self) -> None:
        """문제(질문)만 목록으로 출력한다. 정답은 노출하지 않는다."""
        if not self.quizzes:
            print("\n📋 등록된 퀴즈가 없습니다.")
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("----------------------------------------")
        for i, q in enumerate(self.quizzes, 1):
            print(f"[{i}] {q.question}")
        print("----------------------------------------")

    def _show_best_score(self) -> None:
        """최고 점수(백분율)와 당시 정답/총문항 정보를 출력한다."""
        best_score = self.state.get("best_score")
        if best_score is None:
            print("\n🏆 아직 최고 점수가 없습니다. 먼저 퀴즈를 풀어보세요.")
            return
        bc = self.state.get("best_correct")
        bt = self.state.get("best_total")
        print(f"\n🏆 최고 점수: {best_score}점 ({bt}문제 중 {bc}문제 정답)")

    def _add_quiz(self) -> None:
        """사용자 입력으로 퀴즈 1개를 추가하고 state.json에 반영한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = prompt_nonempty("문제를 입력하세요: ")
        choices: list[str] = []
        for i in range(1, 5):
            choices.append(prompt_nonempty(f"선택지 {i}: "))
        answer = self._prompt_answer()
        hint = input("힌트(없으면 Enter): ").strip() or None

        new_quiz = Quiz(question, choices, answer, hint=hint)
        self.quizzes.append(new_quiz)
        self.state["quizzes"] = [quiz_to_dict(q) for q in self.quizzes]
        if save_state(self.state, STATE_PATH):
            print("✅ 퀴즈가 추가되었습니다!")

    def _delete_quiz(self) -> None:
        """번호를 선택해 퀴즈 1개를 삭제하고 state.json에 반영한다."""
        if not self.quizzes:
            print("\n삭제할 퀴즈가 없습니다.")
            return
        self._list_quizzes()
        idx = prompt_int_in_range("삭제할 퀴즈 번호: ", 1, len(self.quizzes))
        removed = self.quizzes.pop(idx - 1)
        self.state["quizzes"] = [quiz_to_dict(q) for q in self.quizzes]
        if save_state(self.state, STATE_PATH):
            print(f"🗑️ 삭제했습니다: {removed.question}")

    def _show_history(self) -> None:
        """최근 플레이 기록 10개를 간단히 출력한다."""
        history = self.state.get("history") or []
        if not history:
            print("\n기록이 없습니다. 먼저 퀴즈를 풀어보세요.")
            return
        print(f"\n🕒 플레이 기록 (총 {len(history)}회, 최근 10개)")
        print("----------------------------------------")
        for item in history[-10:]:
            ts = item.get("timestamp")
            total = item.get("total")
            correct = item.get("correct")
            score_pct = item.get("score_pct")
            hint_used = item.get("hint_used", 0)
            print(f"- {ts} | {correct}/{total} | {score_pct}점 | 힌트 {hint_used}회")
        print("----------------------------------------")

    def run(self) -> None:
        """메인 메뉴 루프. Ctrl+C/EOF는 안전하게 종료/복귀하도록 처리한다."""
        while True:
            print("\n========================================")
            print("       🎯 나만의 퀴즈 게임 🎯")
            print("========================================")
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 퀴즈 목록")
            print("4. 점수 확인")
            print("5. 퀴즈 삭제")
            print("6. 기록 보기")
            print("7. 종료")
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
            elif choice == 2:
                try:
                    self._add_quiz()
                except (KeyboardInterrupt, EOFError):
                    print("\n\n입력이 중단되었습니다. 메뉴로 돌아갑니다.")
            elif choice == 3:
                self._list_quizzes()
            elif choice == 4:
                self._show_best_score()
            elif choice == 5:
                try:
                    self._delete_quiz()
                except (KeyboardInterrupt, EOFError):
                    print("\n\n입력이 중단되었습니다. 메뉴로 돌아갑니다.")
            elif choice == 6:
                self._show_history()
            elif choice == 7:
                print("\n종료합니다.")
                break
