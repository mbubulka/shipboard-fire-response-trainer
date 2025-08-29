"""
DCA Assessment Manager for the main web server
"""
from typing import Dict, List, Optional
import json

class DCAQuestionState:
    def __init__(self, scenario: str, question: str, options: List[str], correct: int):
        self.scenario = scenario
        self.question = question
        self.options = options
        self.correct = correct
        self.selected_answer: Optional[int] = None
        self.response_time_ms: Optional[int] = None
        self.ai_feedback: Optional[str] = None
        self.ai_confidence: Optional[float] = None

class DCAAssessmentManager:
    def __init__(self):
        self.questions = [
            DCAQuestionState(
                scenario="Initial Response",
                question="You receive a report of smoke in the forward engine room. What is your first action?",
                options=[
                    "Sound general quarters",
                    "Notify the bridge",
                    "Send an investigator",
                    "Activate fire suppression"
                ],
                correct=1  # Notify the bridge
            ),
            DCAQuestionState(
                scenario="Investigation Phase",
                question="The investigator reports active fire in electrical panel 2B. What is your immediate response?",
                options=[
                    "Order immediate evacuation",
                    "Direct CO2 release",
                    "Send in fire team with PKP",
                    "Activate sprinkler system"
                ],
                correct=2  # Send in fire team with PKP
            ),
        ]
        self.current_index = 0
        self.score = 0
        self.responses: List[Dict] = []

    def get_current_question(self) -> Optional[DCAQuestionState]:
        if 0 <= self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None

    def submit_answer(self, selected: int, response_time_ms: int) -> Dict:
        current_question = self.get_current_question()
        if not current_question:
            return {"error": "No current question"}

        current_question.selected_answer = selected
        current_question.response_time_ms = response_time_ms

        is_correct = selected == current_question.correct
        if is_correct:
            self.score += 1

        response_data = {
            "question_index": self.current_index,
            "scenario": current_question.scenario,
            "selected": selected,
            "correct": current_question.correct,
            "is_correct": is_correct,
            "response_time_ms": response_time_ms,
            "score": self.score
        }

        self.responses.append(response_data)
        self.current_index += 1

        return response_data

    def get_final_score(self) -> Dict:
        return {
            "total_questions": len(self.questions),
            "correct_answers": self.score,
            "percentage": (self.score / len(self.questions)) * 100 if self.questions else 0,
            "responses": self.responses
        }

    def reset(self):
        self.current_index = 0
        self.score = 0
        self.responses = []
        for question in self.questions:
            question.selected_answer = None
            question.response_time_ms = None
            question.ai_feedback = None
            question.ai_confidence = None
