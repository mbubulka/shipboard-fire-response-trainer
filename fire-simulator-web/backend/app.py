"""
Flask server to serve the DCA assessment web interface
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys

# Add src directory to path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from dca_question_states import DCAAssessmentManager
from dca_response_evaluator import SimpleResponseEvaluator

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize our assessment system
assessment_manager = DCAAssessmentManager()
evaluator = SimpleResponseEvaluator()

@app.route('/')
def index():
    """Serve the main assessment page"""
    return send_from_directory('.', 'comprehensive.html')

@app.route('/api/evaluate', methods=['POST'])
def evaluate_response():
    """Evaluate a DCA response"""
    data = request.json
    
    # Get the current question
    question = assessment_manager.get_current_question()
    if not question:
        return jsonify({'error': 'No active question'}), 404
    
    # Submit and evaluate the answer
    response_data = assessment_manager.submit_answer(
        data['selectedAnswer'],
        data['responseTime']
    )
    
    # Get DQN evaluation
    evaluation = evaluator.evaluate_response(
        question.scenario,
        response_data,
        {'phase': question.scenario}
    )
    
    return jsonify(evaluation)

if __name__ == '__main__':
    # Run in debug mode
    app.run(debug=True, port=5000)
