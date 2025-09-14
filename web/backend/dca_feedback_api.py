#!/usr/bin/env python3
"""
DCA Feedback Web API Integration
Web endpoints for collecting and managing DCA assessment feedback
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import our feedback system
try:
    from dca_feedback_system import DCAFeedbackCollector, DCAFeedbackAnalyzer, DCAModelRetrainer
except ImportError:
    print("⚠️  DCA Feedback system not available")

app = Flask(__name__)
CORS(app)

# Global feedback system instances
feedback_collector = None
feedback_analyzer = None
model_retrainer = None

def initialize_feedback_system():
    """Initialize the DCA feedback system"""
    global feedback_collector, feedback_analyzer, model_retrainer
    
    try:
        feedback_collector = DCAFeedbackCollector()
        feedback_analyzer = DCAFeedbackAnalyzer()
        model_retrainer = DCAModelRetrainer()
        print("✅ DCA Feedback system initialized")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize feedback system: {e}")
        return False

@app.route('/api/dca/feedback/start_session', methods=['POST'])
def start_feedback_session():
    """Start a new DCA assessment session for feedback collection"""
    
    if not feedback_collector:
        return jsonify({'error': 'Feedback system not initialized'}), 500
    
    try:
        data = request.get_json() or {}
        
        session_data = {
            'user_id': data.get('user_id', 'anonymous'),
            'scenario_id': data.get('scenario_id'),
            'scenario_source': data.get('scenario_source'),
            'scenario_category': data.get('scenario_category'),
            'start_time': datetime.now().isoformat(),
            'difficulty_level': data.get('difficulty_level', 'medium')
        }
        
        session_id = feedback_collector.log_assessment_session(session_data)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Feedback session started',
            'feedback_enabled': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dca/feedback/log_action', methods=['POST'])
def log_assessment_action():
    """Log an individual action during DCA assessment"""
    
    if not feedback_collector:
        return jsonify({'error': 'Feedback system not initialized'}), 400
    
    try:
        data = request.get_json()
        
        action_data = {
            'session_id': data.get('session_id'),
            'step_number': data.get('step_number'),
            'scenario_state': data.get('scenario_state'),
            'ai_recommendation': data.get('ai_recommendation'),
            'ai_confidence': data.get('ai_confidence', 0.5),
            'user_action': data.get('user_action'),
            'action_timestamp': datetime.now().isoformat(),
            'time_taken_seconds': data.get('time_taken_seconds', 0),
            'immediate_reward': data.get('immediate_reward', 0)
        }
        
        action_id = feedback_collector.log_assessment_action(action_data)
        
        return jsonify({
            'success': True,
            'action_id': action_id,
            'message': 'Action logged for feedback analysis'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dca/feedback/submit_feedback', methods=['POST'])
def submit_user_feedback():
    """Submit user feedback on AI recommendations or assessment outcomes"""
    
    if not feedback_collector:
        return jsonify({'error': 'Feedback system not initialized'}), 400
    
    try:
        data = request.get_json()
        
        feedback_data = {
            'session_id': data.get('session_id'),
            'action_id': data.get('action_id'),
            'feedback_type': data.get('feedback_type', 'recommendation'),
            'feedback_rating': data.get('feedback_rating'),  # 1-5 scale
            'feedback_text': data.get('feedback_text', ''),
            'feedback_category': data.get('feedback_category', 'general'),
            'expert_validation': data.get('expert_validation')  # 'approved', 'rejected', None
        }
        
        feedback_id = feedback_collector.collect_user_feedback(feedback_data)
        
        return jsonify({
            'success': True,
            'feedback_id': feedback_id,
            'message': 'Thank you for your feedback!',
            'will_improve_model': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dca/feedback/complete_session', methods=['POST'])
def complete_feedback_session():
    """Complete a DCA assessment session with final metrics"""
    
    if not feedback_collector:
        return jsonify({'error': 'Feedback system not initialized'}), 400
    
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        # Update session with completion data
        with sqlite3.connect(feedback_collector.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE assessment_sessions 
                SET end_time = ?, completion_status = ?, final_score = ?
                WHERE session_id = ?
            """, (
                datetime.now().isoformat(),
                data.get('completion_status', 'completed'),
                data.get('final_score', 0),
                session_id
            ))
            conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Session completed and logged for analysis',
            'session_id': session_id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dca/feedback/analysis', methods=['GET'])
def get_feedback_analysis():
    """Get analysis of recent feedback data"""
    
    if not feedback_analyzer:
        return jsonify({'error': 'Feedback analyzer not available'}), 500
    
    try:
        days_back = request.args.get('days', 30, type=int)
        
        analysis = feedback_analyzer.analyze_ai_recommendation_accuracy(days_back)
        improvement_areas = feedback_analyzer.identify_improvement_areas()
        
        return jsonify({
            'success': True,
            'analysis_period_days': days_back,
            'recommendation_accuracy': analysis,
            'improvement_areas': improvement_areas,
            'generated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dca/feedback/training_recommendations', methods=['GET'])
def get_training_recommendations():
    """Get recommendations for model retraining"""
    
    if not model_retrainer:
        return jsonify({'error': 'Model retrainer not available'}), 500
    
    try:
        should_retrain, retrain_info = model_retrainer.should_retrain_model()
        recommendations = feedback_analyzer.generate_training_recommendations()
        config = model_retrainer.generate_retraining_config()
        
        return jsonify({
            'success': True,
            'should_retrain': should_retrain,
            'retrain_info': retrain_info,
            'training_recommendations': recommendations,
            'retraining_config': config,
            'generated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dca/feedback/metrics', methods=['GET'])
def get_feedback_metrics():
    """Get current feedback system metrics"""
    
    if not feedback_collector:
        return jsonify({'error': 'Feedback system not initialized'}), 500
    
    try:
        db_path = feedback_collector.db_path
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Get basic counts
            cursor.execute("SELECT COUNT(*) FROM assessment_sessions")
            total_sessions = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM assessment_actions")
            total_actions = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM user_feedback")
            total_feedback = cursor.fetchone()[0]
            
            # Get recent activity (last 7 days)
            cursor.execute("""
                SELECT COUNT(*) FROM assessment_sessions 
                WHERE created_at >= date('now', '-7 days')
            """)
            recent_sessions = cursor.fetchone()[0]
            
            # Get feedback rating distribution
            cursor.execute("""
                SELECT feedback_rating, COUNT(*) 
                FROM user_feedback 
                GROUP BY feedback_rating
            """)
            rating_distribution = dict(cursor.fetchall())
        
        metrics = {
            'total_sessions': total_sessions,
            'total_actions': total_actions,
            'total_feedback_items': total_feedback,
            'recent_sessions_7d': recent_sessions,
            'feedback_rating_distribution': rating_distribution,
            'feedback_collection_rate': (total_feedback / total_actions * 100) if total_actions > 0 else 0,
            'system_status': 'operational'
        }
        
        return jsonify({
            'success': True,
            'metrics': metrics,
            'generated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dca/feedback/export_data', methods=['GET'])
def export_feedback_data():
    """Export feedback data for external analysis"""
    
    if not feedback_collector:
        return jsonify({'error': 'Feedback system not initialized'}), 500
    
    try:
        days_back = request.args.get('days', 30, type=int)
        include_pii = request.args.get('include_pii', 'false').lower() == 'true'
        
        db_path = feedback_collector.db_path
        
        with sqlite3.connect(db_path) as conn:
            # Export sessions
            if include_pii:
                session_query = """
                    SELECT * FROM assessment_sessions 
                    WHERE created_at >= date('now', '-{} days')
                """.format(days_back)
            else:
                session_query = """
                    SELECT session_id, scenario_id, scenario_source, scenario_category,
                           start_time, end_time, completion_status, final_score, difficulty_level
                    FROM assessment_sessions 
                    WHERE created_at >= date('now', '-{} days')
                """.format(days_back)
            
            cursor = conn.cursor()
            cursor.execute(session_query)
            sessions = [dict(zip([col[0] for col in cursor.description], row)) 
                       for row in cursor.fetchall()]
            
            # Export actions
            cursor.execute("""
                SELECT aa.* FROM assessment_actions aa
                JOIN assessment_sessions asess ON aa.session_id = asess.session_id
                WHERE asess.created_at >= date('now', '-{} days')
            """.format(days_back))
            actions = [dict(zip([col[0] for col in cursor.description], row)) 
                      for row in cursor.fetchall()]
            
            # Export feedback
            cursor.execute("""
                SELECT uf.* FROM user_feedback uf
                JOIN assessment_sessions asess ON uf.session_id = asess.session_id
                WHERE asess.created_at >= date('now', '-{} days')
            """.format(days_back))
            feedback = [dict(zip([col[0] for col in cursor.description], row)) 
                       for row in cursor.fetchall()]
        
        export_data = {
            'export_info': {
                'generated_at': datetime.now().isoformat(),
                'days_included': days_back,
                'includes_pii': include_pii,
                'total_sessions': len(sessions),
                'total_actions': len(actions),
                'total_feedback': len(feedback)
            },
            'sessions': sessions,
            'actions': actions,
            'feedback': feedback
        }
        
        return jsonify({
            'success': True,
            'data': export_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dca/feedback/status', methods=['GET'])
def get_feedback_system_status():
    """Get current status of the feedback system"""
    
    status = {
        'feedback_collector_available': feedback_collector is not None,
        'feedback_analyzer_available': feedback_analyzer is not None,
        'model_retrainer_available': model_retrainer is not None,
        'database_accessible': False,
        'system_health': 'unknown'
    }
    
    # Test database connectivity
    if feedback_collector:
        try:
            with sqlite3.connect(feedback_collector.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                status['database_accessible'] = True
                status['system_health'] = 'operational'
        except Exception:
            status['system_health'] = 'database_error'
    
    return jsonify({
        'success': True,
        'status': status,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🔥 DCA Feedback Web API")
    print("=" * 40)
    
    # Initialize feedback system
    if initialize_feedback_system():
        print("✅ Feedback system ready")
        print("🚀 Starting web server...")
        app.run(debug=True, port=5002)
    else:
        print("❌ Failed to start feedback system")
        print("💡 Check dca_feedback_system.py dependencies")
