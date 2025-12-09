"""
Response evaluator for DCA decisions
"""
from typing import Dict, List
import json


class DecisionEvaluator:
    def __init__(self):
        # Define scoring weights for different aspects
        self.evaluation_weights = {
            "INITIAL_RESPONSE": {
                "protocol_adherence": 0.4,
                "situation_control": 0.3,
                "risk_management": 0.3
            },
            "ELECTRICAL_FIRE": {
                "protocol_adherence": 0.3,
                "situation_control": 0.4,
                "risk_management": 0.3
            }
        }

    def evaluate_decision(self, 
                         scenario_id: str,
                         consequences: Dict,
                         fire_state: Dict) -> Dict:
        """
        Evaluate a DCA decision based on consequences and fire state
        """
        # Calculate scores for different aspects
        situation_control = self._evaluate_control(
            consequences["effectiveness"],
            fire_state["contained"]
        )
        
        risk_score = self._evaluate_risks(
            consequences["new_risks"],
            fire_state["affected_compartments"],
            fire_state["smoke_spread"]
        )

        protocol_score = self._evaluate_protocol_adherence(
            consequences["state_changes"],
            scenario_id
        )

        # Get weights for this scenario
        weights = self.evaluation_weights.get(
            scenario_id, 
            self.evaluation_weights["INITIAL_RESPONSE"]
        )

        # Calculate total score
        total_score = (
            weights["protocol_adherence"] * protocol_score +
            weights["situation_control"] * situation_control +
            weights["risk_management"] * risk_score
        )

        # Generate feedback
        feedback = self._generate_feedback(
            consequences["state_changes"],
            consequences["new_risks"],
            total_score,
            fire_state["contained"]
        )

        return {
            "score": round(total_score, 2),
            "feedback": feedback,
            "details": {
                "protocol_score": round(protocol_score, 2),
                "control_score": round(situation_control, 2),
                "risk_management": round(risk_score, 2)
            }
        }

    def _evaluate_control(self, effectiveness: float, contained: bool) -> float:
        """Evaluate how well the situation is controlled"""
        base_score = effectiveness
        if contained:
            base_score = min(1.0, base_score + 0.2)
        return base_score

    def _evaluate_risks(self, new_risks: List[str], 
                       affected_areas: List[str],
                       smoke_spread: List[str]) -> float:
        """Evaluate risk management"""
        base_score = 1.0
        
        # Deduct for new risks introduced
        base_score -= len(new_risks) * 0.2
        
        # Deduct for fire/smoke spread
        spread_penalty = (
            (len(affected_areas) - 1) * 0.15 + 
            len(smoke_spread) * 0.1
        )
        base_score -= spread_penalty
        
        return max(0.0, base_score)

    def _evaluate_protocol_adherence(self, 
                                   state_changes: List[str],
                                   scenario_id: str) -> float:
        """Evaluate adherence to proper protocols"""
        score = 1.0
        
        # Check for protocol indicators in state changes
        protocol_indicators = {
            "INITIAL_RESPONSE": [
                "command informed",
                "situational awareness"
            ],
            "ELECTRICAL_FIRE": [
                "fire team",
                "contained",
                "electrical fire"
            ]
        }
        
        indicators = protocol_indicators.get(scenario_id, [])
        matches = sum(
            any(ind.lower() in change.lower() 
                for ind in indicators)
            for change in state_changes
        )
        
        if not matches:
            score *= 0.6
        elif matches < len(indicators):
            score *= 0.8
            
        return score

    def _generate_feedback(self, state_changes: List[str],
                         new_risks: List[str],
                         total_score: float,
                         contained: bool) -> str:
        """Generate detailed feedback"""
        feedback_parts = []
        
        # Overall assessment
        if total_score >= 0.9:
            feedback_parts.append(
                "Excellent decision showing strong command and control."
            )
        elif total_score >= 0.7:
            feedback_parts.append(
                "Good decision with some room for optimization."
            )
        else:
            feedback_parts.append(
                "Decision needs improvement. Consider alternative approaches."
            )

        # State changes feedback
        if state_changes:
            feedback_parts.append(
                f"Situation changes: {'; '.join(state_changes)}."
            )

        # Risk feedback
        if new_risks:
            feedback_parts.append(
                f"New risks introduced: {'; '.join(new_risks)}."
            )

        # Containment feedback
        if contained:
            feedback_parts.append(
                "Fire successfully contained. Maintain control measures."
            )
        else:
            feedback_parts.append(
                "Fire not yet contained. Consider additional measures."
            )

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
