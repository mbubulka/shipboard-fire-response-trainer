#!/usr/bin/env python3
"""
DCA Assessment API Endpoints
Handles evaluation of DCA responses and provides feedback
"""

from flask import Blueprint, request, jsonify
from dca_question_states import DCAQuestionStates
from dca_response_evaluator import DCAResponseEvaluator
import torch

# Create Blueprint for DCA endpoints
dca_api = Blueprint('dca_api', __name__)

# Initialize our evaluation systems
question_states = DCAQuestionStates()
response_evaluator = DCAResponseEvaluator()

# Load trained model if available
try:
    model_path = 'models/dca_response_model.pth'
    response_evaluator.load_state_dict(torch.load(model_path))
    response_evaluator.eval()
    print("✅ Loaded DCA response model")
except Exception as e:
    print(f"⚠️ Could not load DCA model: {e}")

@dca_api.route('/api/dca/evaluate', methods=['POST'])
def evaluate_dca_response():
    """
    Evaluate a DCA response choice and return consequences
    """
    try:
        data = request.get_json()
        
        if not all(k in data for k in ['question_id', 'choice', 'current_state']):
            return jsonify({
                'error': 'Missing required fields'
            }), 400

        # Get base evaluation from question states
        base_eval = question_states.evaluate_choice(
            data['question_id'],
            data['choice'],
            data['current_state']
        )
        
        # Get DQN evaluation
        dqn_eval = response_evaluator.evaluate_response(
            data['question_id'],
            data['choice'],
            data['current_state']
        )
        
        # Combine evaluations
        response = {
            'new_state': base_eval['new_state'],
            'consequence': {
                'time_penalty': base_eval['consequence']['time_penalty'],
                'explanation': base_eval['consequence']['explanation'],
                'risk_level': dqn_eval['confidence']
            },
            'is_optimal': base_eval['is_optimal'],
            'optimal_choice': base_eval['optimal'],
            'dqn_evaluation': {
                'confidence': dqn_eval['confidence'],
                'value': dqn_eval['dqn_value']
            }
        }
        
        return jsonify(response)

    except ValueError as ve:
        return jsonify({
            'error': str(ve)
        }), 400
    except Exception as e:
        print(f"Error evaluating DCA response: {e}")
        return jsonify({
            'error': 'Internal server error'
        }), 500

@dca_api.route('/api/dca/question/<question_id>', methods=['GET'])
def get_question(question_id):
    """
    Get details for a specific question
    """
    try:
        question = question_states.get_question_details(question_id)
        return jsonify(question)
    except ValueError as ve:
        return jsonify({
            'error': str(ve)
        }), 404
    except Exception as e:
        print(f"Error getting question: {e}")
        return jsonify({
            'error': 'Internal server error'
        }), 500
