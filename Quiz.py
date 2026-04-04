class Quiz:
    """
    Quiz 클래스는 퀴즈 문제를 관리하는 클래스입니다.
    Args:
        question (str): 퀴즈 질문
        choices (list): 4개의 선택지 리스트
        answer (int): 정답(1~4 중 하나)
    """
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self, number):
        """문제를 화면에 출력합니다."""
        print(f"\n[문제 {number}]")
        print(self.question)
        for i, choice in enumerate(self.choices, 1):
            print(f"{i}. {choice}")

    def is_correct(self, user_input):
        """사용자 입력이 정답인지 확인합니다."""
        return user_input == self.answer

    