"""
Test script for local DCA assessment system
"""
import os
import json
from datetime import datetime
from dca_question_states import DCAAssessmentManager
from dca_response_evaluator import SimpleResponseEvaluator


def run_test_session():
    # Initialize the assessment manager
    manager = DCAAssessmentManager()
    evaluator = SimpleResponseEvaluator()
    
    # Create results directory if it doesn't exist
    results_dir = "assessment_results"
    os.makedirs(results_dir, exist_ok=True)
    
    # Simulate going through questions
    while question := manager.get_current_question():
        print(f"\nScenario: {question.scenario}")
        print(f"Question: {question.question}")
        
        for i, option in enumerate(question.options):
            print(f"{i}: {option}")
        
        # Simulate user input (for testing, we'll use the correct answer)
        selected = question.correct
        response_time = 4000  # Simulated response time in ms
        
        # Submit the answer
        response = manager.submit_answer(selected, response_time)
        
        # Get DQN evaluation
        evaluation = evaluator.evaluate_response(
            question.scenario,
            response,
            {"phase": question.scenario}
        )
        
        print("\nEvaluation:")
        print(f"Score: {evaluation['score']}")
        print(f"Confidence: {evaluation['confidence']}")
        print(f"Feedback: {evaluation['feedback']}")
        print("=" * 50)
    
    # Get final results
    results = manager.get_final_results()
    print("\nFinal Results:")
    print(f"Score: {results['percentage']}%")
    print(f"Correct: {results['correct_answers']} / {results['total_questions']}")
    
    # Save session data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_file = os.path.join(results_dir, f"session_{timestamp}.json")
    manager.save_session(session_file)
    
    # Save evaluations
    evals_file = os.path.join(results_dir, f"evaluations_{timestamp}.json")
    evaluator.save_evaluation(evals_file, {
        'timestamp': timestamp,
        'results': results,
        'evaluations': [
            evaluator.evaluate_response(
                r['scenario'], 
                r, 
                {'phase': r['scenario']}
            )
            for r in results['responses']
        ]
    })
    
    print(f"\nSession data saved to: {session_file}")
    print(f"Evaluations saved to: {evals_file}")


if __name__ == "__main__":
    run_test_session()
