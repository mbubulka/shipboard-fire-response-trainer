"""
DCA Question States and Management Module
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
            # Add more questions as needed
        ]
        self.current_index = 0
        self.score = 0
        self.responses: List[Dict] = []

    def get_current_question(self) -> Optional[DCAQuestionState]:
        if 0 <= self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None

    def submit_answer(self, answer_index: int, response_time_ms: int) -> Dict:
        question = self.get_current_question()
        if question:
            question.selected_answer = answer_index
            question.response_time_ms = response_time_ms
            
            # Store response data
            response_data = {
                'scenario': question.scenario,
                'question': question.question,
                'selected': question.options[answer_index],
                'correct': answer_index == question.correct,
                'response_time_ms': response_time_ms
            }
            self.responses.append(response_data)
            
            # Update score
            if answer_index == question.correct:
                self.score += 1
            
            # Move to next question
            self.current_index += 1
            
            return response_data
        return {}

    def get_final_results(self) -> Dict:
        return {
            'total_questions': len(self.questions),
            'correct_answers': self.score,
            'percentage': (self.score / len(self.questions)) * 100,
            'responses': self.responses
        }

    def save_session(self, filepath: str):
        """Save the current session data to a JSON file"""
        session_data = {
            'score': self.score,
            'total_questions': len(self.questions),
            'responses': self.responses
        }
        with open(filepath, 'w') as f:
            json.dump(session_data, f, indent=2)

    @classmethod
    def load_session(cls, filepath: str) -> 'DCAAssessmentManager':
        """Load a session from a JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        manager = cls()
        manager.score = data['score']
        manager.responses = data['responses']
        return manager
