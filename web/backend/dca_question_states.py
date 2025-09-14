#!/usr/bin/env python3
"""
DCA Question States and Evaluation System
Defines question states, choices, and consequences for DCA training
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple
import numpy as np

class ScenarioState(Enum):
    INITIAL = "initial"
    FIRE_CONTAINED = "fire_contained"
    FIRE_SPREAD = "fire_spread"
    DELAYED_RESPONSE = "delayed_response"
    OPTIMAL_RESPONSE = "optimal_response"

class DCAQuestionStates:
    def __init__(self):
        # Define base states for fire scenarios
        self.base_states = {
            "fire_location": None,
            "smoke_condition": "none",  # none, light, moderate, heavy
            "time_elapsed": 0,
            "compartments_affected": [],
            "boundaries_set": False,
            "investigators_deployed": False,
            "fedfire_arrived": False
        }

        # Define question states and their consequences
        self.question_states = {
            "initial_response": {
                "question": "What is your initial response to the reported fire?",
                "choices": [
                    "A. Wait for FEDFIRE to arrive",
                    "B. Deploy investigators immediately",
                    "C. Evacuate the entire compartment",
                    "D. Set fire boundaries and deploy investigators"
                ],
                "consequences": {
                    "A": {
                        "risk_increase": 0.8,
                        "next_state": ScenarioState.FIRE_SPREAD,
                        "time_penalty": 15,
                        "state_changes": {
                            "smoke_condition": "heavy",
                            "fedfire_arrived": True
                        },
                        "explanation": "Waiting for FEDFIRE allows fire to grow and spread"
                    },
                    "B": {
                        "risk_increase": 0.3,
                        "next_state": ScenarioState.FIRE_CONTAINED,
                        "time_penalty": 5,
                        "state_changes": {
                            "investigators_deployed": True
                        },
                        "explanation": "Quick response but boundaries not set"
                    },
                    "C": {
                        "risk_increase": 0.4,
                        "next_state": ScenarioState.DELAYED_RESPONSE,
                        "time_penalty": 10,
                        "state_changes": {
                            "smoke_condition": "moderate"
                        },
                        "explanation": "Evacuation good but delays fire response"
                    },
                    "D": {
                        "risk_increase": 0.1,
                        "next_state": ScenarioState.OPTIMAL_RESPONSE,
                        "time_penalty": 7,
                        "state_changes": {
                            "boundaries_set": True,
                            "investigators_deployed": True
                        },
                        "explanation": "Optimal response: Contains fire and gathers intel"
                    }
                },
                "optimal_choice": "D"
            }
        }

    def evaluate_choice(self, question_id: str, choice: str, current_state: Dict) -> Dict:
        """
        Evaluate a user's choice for a specific question
        Returns consequences and new state
        """
        if question_id not in self.question_states:
            raise ValueError(f"Unknown question ID: {question_id}")

        question = self.question_states[question_id]
        if choice not in question["consequences"]:
            raise ValueError(f"Invalid choice {choice} for question {question_id}")

        consequence = question["consequences"][choice]
        
        # Create new state by applying consequences
        new_state = current_state.copy()
        new_state["time_elapsed"] += consequence["time_penalty"]
        
        for key, value in consequence["state_changes"].items():
            new_state[key] = value

        return {
            "selected": choice,
            "optimal": question["optimal_choice"],
            "consequence": consequence,
            "new_state": new_state,
            "is_optimal": choice == question["optimal_choice"]
        }

    def get_question_details(self, question_id: str) -> Dict:
        """Get all details for a specific question"""
        if question_id not in self.question_states:
            raise ValueError(f"Unknown question ID: {question_id}")
        
        return self.question_states[question_id]

    def initialize_scenario_state(self, fire_location: str) -> Dict:
        """Initialize a new scenario state"""
        state = self.base_states.copy()
        state["fire_location"] = fire_location
        state["compartments_affected"] = [fire_location]
        state["smoke_condition"] = "light"
        return state
