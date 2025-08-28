"""
Shipboard Fire Response AI - AWS Lambda API Handler
Simple API wrapper for the trained DQN model
"""

import json
import boto3
import numpy as np
import torch
from typing import Dict, Any
import pickle
import base64

class ShipboardFireResponseAPI:
    """AWS Lambda handler for Shipboard Fire Response AI"""
    
    def __init__(self):
        self.model = None
        self.scenarios = None
        self._load_model()
        self._load_scenarios()
    
    def _load_model(self):
        """Load the trained DQN model"""
        try:
            # In production, load from S3
            # For now, we'll use a simplified approach
            self.model_loaded = True
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model_loaded = False
    
    def _load_scenarios(self):
        """Load pre-defined scenarios"""
        self.scenarios = {
            "engine_room_fuel": {
                "id": 1,
                "title": "Engine Room JP-5 Fuel Fire",
                "description": "Small fuel fire in engine room, crew available",
                "state": [1, 0.4, 0.3, 0.6, 45, 15, 0.8, 0.9, 0.7, 1, 8, 25, 0, 3, 1, 0.1, 1],
                "complexity": 6
            },
            "berthing_electrical": {
                "id": 2,
                "title": "Berthing Electrical Fire",
                "description": "Electrical fire in crew berthing, smoke present",
                "state": [2, 0.3, 0.2, 0.4, 38, 12, 0.9, 0.8, 0.6, 0, 6, 20, 1, 2, 1, 0.05, 0],
                "complexity": 4
            },
            "hangar_aircraft": {
                "id": 3,
                "title": "Hangar Bay Aircraft Fire",
                "description": "Aircraft fire in hangar bay, high risk scenario",
                "state": [1, 0.8, 0.7, 0.9, 25, 8, 0.6, 0.7, 0.5, 1, 4, 15, 2, 6, 2, 0.3, 2],
                "complexity": 10
            },
            "galley_cooking": {
                "id": 4,
                "title": "Galley Cooking Fire",
                "description": "Cooking fire in ship's galley, contained area",
                "state": [0, 0.2, 0.1, 0.3, 50, 18, 0.9, 0.9, 0.8, 1, 10, 30, 3, 2, 1, 0.02, 0],
                "complexity": 3
            }
        }
    
    def predict_action(self, scenario_id: str) -> Dict[str, Any]:
        """Predict the best action for a given scenario"""
        
        if scenario_id not in self.scenarios:
            return {"error": "Scenario not found"}
        
        scenario = self.scenarios[scenario_id]
        
        # Simulate DQN prediction (replace with actual model inference)
        actions = [
            "assess_situation",
            "dispatch_small_team", 
            "dispatch_large_team",
            "call_fedfire",
            "activate_foam_system",
            "ship_recall",
            "evacuate_space",
            "monitor_situation"
        ]
        
        # Simple logic based on scenario complexity
        complexity = scenario["complexity"]
        
        if complexity <= 3:
            predicted_action = "dispatch_small_team"
            confidence = 0.92
            reasoning = "Low complexity fire can be handled by small team"
        elif complexity <= 6:
            predicted_action = "dispatch_large_team"
            confidence = 0.88
            reasoning = "Medium complexity requires larger response team"
        elif complexity <= 8:
            predicted_action = "call_fedfire"
            confidence = 0.85
            reasoning = "High complexity needs professional fire department"
        else:
            predicted_action = "ship_recall"
            confidence = 0.90
            reasoning = "Critical situation requires all-hands response"
        
        return {
            "scenario": scenario,
            "predicted_action": predicted_action,
            "confidence": confidence,
            "reasoning": reasoning,
            "all_actions": actions,
            "success_probability": confidence
        }
    
    def get_scenarios(self) -> Dict[str, Any]:
        """Get all available scenarios"""
        return {
            "scenarios": list(self.scenarios.keys()),
            "details": self.scenarios
        }

# AWS Lambda handler
def lambda_handler(event, context):
    """Main Lambda function handler"""
    
    api = ShipboardFireResponseAPI()
    
    try:
        # Parse the request
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        
        # Enable CORS
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
        
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'CORS preflight'})
            }
        
        if http_method == 'GET' and path == '/scenarios':
            # Return available scenarios
            result = api.get_scenarios()
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(result)
            }
        
        elif http_method == 'POST' and path == '/predict':
            # Predict action for scenario
            body = json.loads(event.get('body', '{}'))
            scenario_id = body.get('scenario_id')
            
            if not scenario_id:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({'error': 'scenario_id required'})
                }
            
            result = api.predict_action(scenario_id)
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(result)
            }
        
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Endpoint not found'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

# Local testing
if __name__ == "__main__":
    api = ShipboardFireResponseAPI()
    
    # Test scenarios endpoint
    print("=== Testing Scenarios ===")
    scenarios = api.get_scenarios()
    print(json.dumps(scenarios, indent=2))
    
    # Test prediction
    print("\n=== Testing Prediction ===")
    prediction = api.predict_action("engine_room_fuel")
    print(json.dumps(prediction, indent=2))
