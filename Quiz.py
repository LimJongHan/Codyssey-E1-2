"""퀴즈 한 문항을 표현하는 모델.

과제 요구사항:
- 선택지는 4개를 기본으로 한다.
- 정답은 1~4 중 번호로 관리한다.

이 모듈은 '문항 표현'에만 집중하고, 입력/저장/게임 루프는 `QuizGame`에서 담당한다.
"""

class Quiz:
    def __init__(self, question, choices, answer, hint=None):
        """
        Args:
            question (str): 퀴즈 질문
            choices (list): 4개의 선택지 리스트
            answer (int): 정답(1~4 중 하나)
            hint (str | None): 힌트(선택). 플레이 중 'h' 입력 시 표시한다.
        """
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def display(self, number):
        """문제와 4지선다 선택지를 화면에 출력한다."""
        print(f"\n[문제 {number}]")
        print(self.question)
        for i, choice in enumerate(self.choices, 1):
            print(f"{i}. {choice}")

    def is_correct(self, user_input):
        """사용자 입력(정답 번호)이 정답인지 반환한다."""
        return user_input == self.answer
