#!/usr/bin/env python3
"""
Web API Integration for DCA Feedback System
Flask endpoints for collecting and analyzing feedback data
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
import uuid
from datetime import datetime
from feedback_system import FeedbackDatabase, FeedbackData, FeedbackAnalyzer

app = Flask(__name__)
CORS(app)

# Global feedback system components
feedback_db = FeedbackDatabase()
feedback_analyzer = FeedbackAnalyzer(feedback_db)

@app.route('/api/feedback/submit', methods=['POST'])
def submit_feedback():
    """Submit user feedback for a completed DCA assessment"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'session_id', 'scenario_id', 'difficulty_rating', 
            'ai_helpfulness', 'scenario_realism', 'confidence_level',
            'training_level'
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Get session data from cache or database
        session_data = get_session_data(data['session_id'])
        if not session_data:
            return jsonify({
                'success': False,
                'error': 'Session data not found'
            }), 404
        
        # Create feedback object
        feedback = FeedbackData(
            session_id=data['session_id'],
            user_id=data.get('user_id', 'anonymous'),
            scenario_id=data['scenario_id'],
            scenario_source=session_data.get('scenario_source', 'unknown'),
            scenario_category=session_data.get('scenario_category', 'unknown'),
            
            # Performance data from session
            actions_taken=session_data.get('actions_taken', []),
            ai_recommendations=session_data.get('ai_recommendations', []),
            user_followed_ai=session_data.get('user_followed_ai', []),
            response_times=session_data.get('response_times', []),
            
            final_score=session_data.get('final_score', 0),
            completion_time=session_data.get('completion_time', 0),
            errors_made=session_data.get('errors_made', 0),
            critical_errors=session_data.get('critical_errors', 0),
            
            # User feedback
            difficulty_rating=int(data['difficulty_rating']),
            ai_helpfulness=int(data['ai_helpfulness']),
            scenario_realism=int(data['scenario_realism']),
            confidence_level=int(data['confidence_level']),
            
            # Qualitative feedback
            what_worked_well=data.get('what_worked_well', ''),
            what_was_confusing=data.get('what_was_confusing', ''),
            suggested_improvements=data.get('suggested_improvements', ''),
            additional_comments=data.get('additional_comments', ''),
            
            # Metadata
            timestamp=datetime.now().isoformat(),
            training_level=data['training_level'],
            previous_experience=data.get('previous_experience', '')
        )
        
        # Store feedback
        feedback_id = feedback_db.store_feedback(feedback)
        
        # Check if retraining should be triggered
        if should_trigger_retraining():
            trigger_model_retraining()
        
        return jsonify({
            'success': True,
            'feedback_id': feedback_id,
            'message': 'Feedback submitted successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/feedback/analytics/summary', methods=['GET'])
def get_feedback_analytics():
    """Get summary analytics from recent feedback"""
    try:
        days = request.args.get('days', 30, type=int)
        
        # Get AI effectiveness analysis
        ai_effectiveness = feedback_analyzer.analyze_ai_recommendation_effectiveness()
        
        # Get difficult scenarios
        difficult_scenarios = feedback_analyzer.identify_difficult_scenarios()
        
        # Get performance by source
        sources = ['nfpa_1500', 'nfpa_1521', 'nfpa_1670', 'uscg', 'navy']
        source_performance = {}
        
        for source in sources:
            perf = feedback_db.get_performance_by_source(source)
            if perf.get('total_sessions', 0) > 0:
                source_performance[source] = perf
        
        # Get improvement recommendations
        recommendations = feedback_analyzer.generate_improvement_recommendations()
        
        return jsonify({
            'success': True,
            'data': {
                'ai_effectiveness': ai_effectiveness,
                'difficult_scenarios': difficult_scenarios[:5],
                'source_performance': source_performance,
                'recommendations': recommendations,
                'analysis_period_days': days
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/feedback/session/start', methods=['POST'])
def start_feedback_session():
    """Start a new feedback session for tracking user actions"""
    try:
        data = request.get_json() or {}
        
        session_id = str(uuid.uuid4())
        
        # Initialize session data
        session_data = {
            'session_id': session_id,
            'scenario_id': data.get('scenario_id'),
            'scenario_source': data.get('scenario_source'),
            'scenario_category': data.get('scenario_category'),
            'user_id': data.get('user_id', 'anonymous'),
            'start_time': datetime.now().isoformat(),
            'actions_taken': [],
            'ai_recommendations': [],
            'user_followed_ai': [],
            'response_times': [],
            'errors_made': 0,
            'critical_errors': 0
        }
        
        # Store session data (in production, use Redis or database)
        store_session_data(session_id, session_data)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Feedback session started'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/feedback/session/action', methods=['POST'])
def log_session_action():
    """Log an action taken during the assessment"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if not session_id:
            return jsonify({
                'success': False,
                'error': 'Session ID required'
            }), 400
        
        session_data = get_session_data(session_id)
        if not session_data:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        # Log the action
        session_data['actions_taken'].append(data.get('action'))
        session_data['ai_recommendations'].append(data.get('ai_recommendation'))
        session_data['user_followed_ai'].append(data.get('followed_ai', False))
        session_data['response_times'].append(data.get('response_time', 0))
        
        # Update error counts
        if data.get('is_error'):
            session_data['errors_made'] += 1
        if data.get('is_critical_error'):
            session_data['critical_errors'] += 1
        
        # Store updated session data
        store_session_data(session_id, session_data)
        
        return jsonify({
            'success': True,
            'message': 'Action logged'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/feedback/session/complete', methods=['POST'])
def complete_session():
    """Complete a feedback session with final score"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if not session_id:
            return jsonify({
                'success': False,
                'error': 'Session ID required'
            }), 400
        
        session_data = get_session_data(session_id)
        if not session_data:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        # Update final session data
        session_data['final_score'] = data.get('final_score', 0)
        session_data['completion_time'] = data.get('completion_time', 0)
        session_data['end_time'] = datetime.now().isoformat()
        
        # Store updated session data
        store_session_data(session_id, session_data)
        
        return jsonify({
            'success': True,
            'message': 'Session completed',
            'feedback_url': f'/feedback/form?session_id={session_id}'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/feedback/form')
def feedback_form():
    """Serve the feedback collection form"""
    session_id = request.args.get('session_id')
    
    if not session_id:
        return "Error: Session ID required", 400
    
    session_data = get_session_data(session_id)
    if not session_data:
        return "Error: Session not found", 404
    
    # Return the feedback form HTML
    return render_template_string(get_feedback_form_html(), 
                                session_id=session_id, 
                                session_data=session_data)

@app.route('/api/feedback/trigger-retraining', methods=['POST'])
def trigger_retraining():
    """Manually trigger model retraining based on recent feedback"""
    try:
        # Get recent feedback
        recent_feedback = feedback_db.get_recent_feedback(days=30)
        
        if len(recent_feedback) < 10:
            return jsonify({
                'success': False,
                'error': 'Insufficient feedback data for retraining'
            }), 400
        
        # Queue retraining job
        feedback_ids = [f['id'] for f in recent_feedback]
        
        # In production, this would queue a background job
        result = queue_model_retraining(feedback_ids)
        
        return jsonify({
            'success': True,
            'message': 'Model retraining queued',
            'job_id': result.get('job_id'),
            'feedback_count': len(feedback_ids)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Helper functions
def get_session_data(session_id: str):
    """Get session data (in production, use Redis or database)"""
    # For now, use a simple file-based storage
    import os
    session_file = f"session_{session_id}.json"
    
    if os.path.exists(session_file):
        with open(session_file, 'r') as f:
            return json.load(f)
    return None

def store_session_data(session_id: str, data: dict):
    """Store session data (in production, use Redis or database)"""
    import os
    session_file = f"session_{session_id}.json"
    
    with open(session_file, 'w') as f:
        json.dump(data, f)

def should_trigger_retraining() -> bool:
    """Check if automatic retraining should be triggered"""
    # Simple heuristic: trigger if AI effectiveness is declining
    ai_effectiveness = feedback_analyzer.analyze_ai_recommendation_effectiveness()
    return ai_effectiveness.get('ai_effectiveness_ratio', 1.0) < 0.85

def trigger_model_retraining():
    """Trigger automatic model retraining"""
    recent_feedback = feedback_db.get_recent_feedback(days=14)
    if len(recent_feedback) >= 5:
        feedback_ids = [f['id'] for f in recent_feedback]
        queue_model_retraining(feedback_ids, priority=2)

def queue_model_retraining(feedback_ids: list, priority: int = 1):
    """Queue a model retraining job"""
    # In production, this would use a job queue like Celery
    print(f"🧠 Queued model retraining with {len(feedback_ids)} feedback samples")
    return {'job_id': str(uuid.uuid4())}

def get_feedback_form_html():
    """Get the feedback form HTML template"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>DCA Assessment Feedback</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .feedback-section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
            .rating-scale { display: flex; gap: 10px; align-items: center; margin: 10px 0; }
            .rating-scale input[type="radio"] { margin: 0 5px; }
            textarea { width: 100%; height: 80px; padding: 8px; margin: 10px 0; }
            select { width: 100%; padding: 8px; margin: 10px 0; }
            button { background: #007cba; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background: #005a87; }
            .required { color: red; }
            h2 { color: #007cba; }
        </style>
    </head>
    <body>
        <h2>🔥 DCA Assessment Feedback</h2>
        <p>Please provide feedback on your training experience to help us improve the system.</p>
        
        <form id="feedbackForm">
            <input type="hidden" name="session_id" value="{{ session_id }}">
            
            <div class="feedback-section">
                <h3>Performance Ratings</h3>
                
                <label>Scenario Difficulty <span class="required">*</span></label>
                <div class="rating-scale">
                    <span>Very Easy</span>
                    <input type="radio" name="difficulty_rating" value="1" required> 1
                    <input type="radio" name="difficulty_rating" value="2"> 2
                    <input type="radio" name="difficulty_rating" value="3"> 3
                    <input type="radio" name="difficulty_rating" value="4"> 4
                    <input type="radio" name="difficulty_rating" value="5"> 5
                    <span>Very Hard</span>
                </div>
                
                <label>AI Helpfulness <span class="required">*</span></label>
                <div class="rating-scale">
                    <span>Not Helpful</span>
                    <input type="radio" name="ai_helpfulness" value="1" required> 1
                    <input type="radio" name="ai_helpfulness" value="2"> 2
                    <input type="radio" name="ai_helpfulness" value="3"> 3
                    <input type="radio" name="ai_helpfulness" value="4"> 4
                    <input type="radio" name="ai_helpfulness" value="5"> 5
                    <span>Very Helpful</span>
                </div>
                
                <label>Scenario Realism <span class="required">*</span></label>
                <div class="rating-scale">
                    <span>Unrealistic</span>
                    <input type="radio" name="scenario_realism" value="1" required> 1
                    <input type="radio" name="scenario_realism" value="2"> 2
                    <input type="radio" name="scenario_realism" value="3"> 3
                    <input type="radio" name="scenario_realism" value="4"> 4
                    <input type="radio" name="scenario_realism" value="5"> 5
                    <span>Very Realistic</span>
                </div>
                
                <label>Your Confidence <span class="required">*</span></label>
                <div class="rating-scale">
                    <span>Not Confident</span>
                    <input type="radio" name="confidence_level" value="1" required> 1
                    <input type="radio" name="confidence_level" value="2"> 2
                    <input type="radio" name="confidence_level" value="3"> 3
                    <input type="radio" name="confidence_level" value="4"> 4
                    <input type="radio" name="confidence_level" value="5"> 5
                    <span>Very Confident</span>
                </div>
            </div>
            
            <div class="feedback-section">
                <h3>Additional Feedback</h3>
                
                <label for="what_worked_well">What worked well?</label>
                <textarea id="what_worked_well" name="what_worked_well" placeholder="What aspects were effective?"></textarea>
                
                <label for="what_was_confusing">What was confusing?</label>
                <textarea id="what_was_confusing" name="what_was_confusing" placeholder="What could be clearer?"></textarea>
                
                <label for="suggested_improvements">Suggested improvements:</label>
                <textarea id="suggested_improvements" name="suggested_improvements" placeholder="How could this be improved?"></textarea>
                
                <label for="additional_comments">Additional comments:</label>
                <textarea id="additional_comments" name="additional_comments" placeholder="Any other feedback?"></textarea>
            </div>
            
            <div class="feedback-section">
                <h3>Background</h3>
                
                <label for="training_level">Experience Level <span class="required">*</span></label>
                <select id="training_level" name="training_level" required>
                    <option value="">Select your level</option>
                    <option value="novice">Novice (< 1 year)</option>
                    <option value="intermediate">Intermediate (1-3 years)</option>
                    <option value="advanced">Advanced (3-10 years)</option>
                    <option value="expert">Expert (> 10 years)</option>
                </select>
                
                <label for="previous_experience">Background:</label>
                <textarea id="previous_experience" name="previous_experience" placeholder="Brief description of your fire response experience..."></textarea>
            </div>
            
            <button type="submit">Submit Feedback</button>
        </form>
        
        <script>
            document.getElementById('feedbackForm').addEventListener('submit', function(e) {
                e.preventDefault();
                
                const formData = new FormData(this);
                const feedback = Object.fromEntries(formData.entries());
                
                fetch('/api/feedback/submit', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(feedback)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Thank you for your feedback!');
                        window.close();
                    } else {
                        alert('Error: ' + data.error);
                    }
                })
                .catch(error => {
                    alert('Error submitting feedback');
                    console.error(error);
                });
            });
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("🔄 Starting DCA Feedback API Server")
    print("📊 Feedback collection endpoints ready")
    print("🔍 Analytics API available")
    print("🚀 Starting on http://localhost:5002")
    
    app.run(debug=True, port=5002)
