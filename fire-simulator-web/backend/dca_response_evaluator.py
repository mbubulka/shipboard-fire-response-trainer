#!/usr/bin/env python3
"""
DCA DQN Evaluator
Evaluates DCA responses using DQN and provides feedback
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Dict, List
from dca_question_states import DCAQuestionStates, ScenarioState


class DCAResponseEvaluator(nn.Module):
    def __init__(self, state_dim: int = 8, action_dim: int = 4):
        super(DCAResponseEvaluator, self).__init__()
        
        self.state_dim = state_dim
        self.action_dim = action_dim
        
        # Neural network layers
        self.fc1 = nn.Linear(state_dim, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, action_dim)
        
        # Question states manager
        self.question_states = DCAQuestionStates()

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)

    def encode_state(self, state: Dict) -> torch.Tensor:
        """Convert scenario state to tensor"""
        # Encode various state elements
        encoded = [
            1 if state["fire_location"] else 0,
            ["none", "light", "moderate", "heavy"].index(state["smoke_condition"]),
            state["time_elapsed"] / 60,  # Normalize time to hours
            len(state["compartments_affected"]),
            1 if state["boundaries_set"] else 0,
            1 if state["investigators_deployed"] else 0,
            1 if state["fedfire_arrived"] else 0,
            0  # Reserved for future use
        ]
        return torch.FloatTensor(encoded)

    def evaluate_response(self, question_id: str, 
                         choice: str, 
                         current_state: Dict) -> Dict:
        """
        Evaluate a response using both DQN and predefined states
        """
        # Get base evaluation from question states
        base_eval = self.question_states.evaluate_choice(
            question_id, choice, current_state
        )
        
        # Get DQN evaluation
        state_tensor = self.encode_state(current_state)
        with torch.no_grad():
            action_values = self(state_tensor)
            
        # Convert choice to index
        choice_idx = ord(choice) - ord('A')
        choice_value = action_values[choice_idx].item()
        
        # Get best action according to DQN
        best_action = chr(ord('A') + torch.argmax(action_values).item())
        
        # Combine evaluations
        evaluation = {
            **base_eval,
            "dqn_value": choice_value,
            "dqn_best_action": best_action,
            "confidence": F.softmax(action_values, dim=0)[choice_idx].item()
        }
        
        return evaluation

    def get_consequences(self, evaluation: Dict) -> str:
        """Generate consequence message based on evaluation"""
        consequence = evaluation["consequence"]
        
        message = f"Time Impact: +{consequence['time_penalty']} minutes\n"
        
        if evaluation["is_optimal"]:
            message += "This was the optimal choice. "
        else:
            message += (f"A better choice would have been option "
                       f"{evaluation['optimal']}. ")
        
        message += consequence["explanation"]
        
        if evaluation["confidence"] < 0.3:
            message += "\nWarning: High risk decision in current conditions."
        
        return message
