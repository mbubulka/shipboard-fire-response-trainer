"""
DCA Response Evaluator using simplified DQN approach
"""
from typing import Dict, List, Tuple
import json
import numpy as np


class SimpleResponseEvaluator:
    def __init__(self):
        # Define scenario weights and features
        self.scenario_weights = {
            "Initial Response": {
                "speed": 0.4,
                "protocol": 0.4,
                "safety": 0.2
            },
            "Investigation Phase": {
                "speed": 0.3,
                "protocol": 0.3,
                "safety": 0.4
            }
        }
        
        # Response time thresholds (ms)
        self.time_thresholds = {
            "Initial Response": {
                "excellent": 3000,
                "good": 5000,
                "acceptable": 8000
            },
            "Investigation Phase": {
                "excellent": 4000,
                "good": 7000,
                "acceptable": 10000
            }
        }

    def evaluate_response(self, 
                         scenario: str,
                         response_data: Dict,
                         context: Dict) -> Dict:
        """
        Evaluate a DCA response using our simplified DQN-like approach
        """
        # Extract features
        time_score = self._evaluate_response_time(
            scenario, 
            response_data["response_time_ms"]
        )
        protocol_score = float(response_data["correct"])
        safety_score = self._evaluate_safety(scenario, response_data)

        # Calculate weighted score
        weights = self.scenario_weights[scenario]
        total_score = (
            weights["speed"] * time_score +
            weights["protocol"] * protocol_score +
            weights["safety"] * safety_score
        )

        # Generate confidence based on feature agreement
        scores = [time_score, protocol_score, safety_score]
        confidence = self._calculate_confidence(scores)

        # Prepare feedback
        feedback = self._generate_feedback(
            scenario,
            total_score,
            time_score,
            protocol_score,
            safety_score
        )

        return {
            "score": round(total_score, 2),
            "confidence": round(confidence, 2),
            "feedback": feedback,
            "details": {
                "time_score": round(time_score, 2),
                "protocol_score": round(protocol_score, 2),
                "safety_score": round(safety_score, 2)
            }
        }

    def _evaluate_response_time(self, scenario: str, 
                              response_time: int) -> float:
        """Calculate normalized score for response time"""
        thresholds = self.time_thresholds[scenario]
        
        if response_time <= thresholds["excellent"]:
            return 1.0
        elif response_time <= thresholds["good"]:
            return 0.8
        elif response_time <= thresholds["acceptable"]:
            return 0.6
        else:
            return 0.4

    def _evaluate_safety(self, scenario: str, 
                        response_data: Dict) -> float:
        """
        Evaluate safety considerations in the response
        Currently uses a simple lookup, could be enhanced with more logic
        """
        # Simple safety scoring based on scenario
        if scenario == "Initial Response":
            return 0.8  # Base safety score for initial response
        elif scenario == "Investigation Phase":
            if response_data["correct"]:
                return 1.0  # Correct response in investigation is safe
            return 0.6  # Incorrect response may have safety implications
        return 0.7  # Default safety score

    def _calculate_confidence(self, scores: List[float]) -> float:
        """
        Calculate confidence based on agreement between different scores
        """
        # Use standard deviation as a measure of score agreement
        std_dev = np.std(scores)
        # Convert to confidence (1 - normalized std_dev)
        confidence = 1 - (std_dev / max(scores))
        return min(max(confidence, 0), 1)  # Clamp between 0 and 1

    def _generate_feedback(self, scenario: str, total_score: float,
                         time_score: float, protocol_score: float,
                         safety_score: float) -> str:
        """Generate human-readable feedback"""
        feedback_parts = []
        
        # Overall assessment
        if total_score >= 0.9:
            feedback_parts.append("Excellent response overall.")
        elif total_score >= 0.7:
            feedback_parts.append("Good response with some room for improvement.")
        else:
            feedback_parts.append("Response needs significant improvement.")

        # Time feedback
        if time_score < 0.6:
            feedback_parts.append("Response time was too slow for this scenario.")
        elif time_score < 0.8:
            feedback_parts.append("Response time was acceptable but could be faster.")
        
        # Protocol feedback
        if protocol_score < 1.0:
            feedback_parts.append("Review standard protocols for this scenario.")
        
        # Safety feedback
        if safety_score < 0.8:
            feedback_parts.append("Consider safety implications more carefully.")

        return " ".join(feedback_parts)

    def save_evaluation(self, filepath: str, evaluation_data: Dict):
        """Save evaluation results to a JSON file"""
        with open(filepath, 'w') as f:
            json.dump(evaluation_data, f, indent=2)

    @classmethod
    def load_evaluations(cls, filepath: str) -> List[Dict]:
        """Load previous evaluations from a JSON file"""
        with open(filepath, 'r') as f:
            return json.load(f)
