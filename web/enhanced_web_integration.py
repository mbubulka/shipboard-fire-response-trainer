#!/usr/bin/env python3
"""
Enhanced Web Training Integration
Integrates enhanced DQN with web-based fire response training
"""

import json
import numpy as np
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Global variables for the enhanced system
enhanced_env = None
enhanced_agent = None
current_session = {}

def initialize_enhanced_system():
    """Initialize the enhanced DQN system"""
    global enhanced_env, enhanced_agent
    
    try:
        from enhanced_dqn_system import (
            EnhancedFireResponseEnvironment,
            EnhancedDQNAgent
        )
        
        # Create environment
        enhanced_env = EnhancedFireResponseEnvironment()
        
        # Create agent
        enhanced_agent = EnhancedDQNAgent(
            state_dim=enhanced_env.state_dim,
            action_dim=enhanced_env.action_dim
        )
        
        # Try to load trained model
        model_path = Path(__file__).parent / "models" / "enhanced_dqn_final.pth"
        if model_path.exists():
            enhanced_agent.load_model(str(model_path))
            enhanced_agent.epsilon = 0.1  # Small exploration for variety
            print("✅ Enhanced DQN system initialized with trained model")
        else:
            print("⚠️  Enhanced DQN system initialized without trained model")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize enhanced system: {e}")
        return False

@app.route('/api/enhanced/start_session', methods=['POST'])
def start_enhanced_session():
    """Start a new enhanced training session"""
    global current_session
    
    if not enhanced_env or not enhanced_agent:
        return jsonify({
            'error': 'Enhanced system not initialized'
        }), 500
    
    try:
        # Get request parameters
        data = request.get_json() or {}
        preferred_source = data.get('source', None)  # nfpa_1500, uscg, navy
        preferred_category = data.get('category', None)  # fire, emergency, etc.
        
        # Filter scenarios if preferences specified
        available_scenarios = enhanced_env.scenarios
        
        if preferred_source:
            available_scenarios = [
                s for s in available_scenarios
                if s.get('source', '').lower() == preferred_source.lower()
            ]
        
        if preferred_category:
            available_scenarios = [
                s for s in available_scenarios
                if s.get('category', '').lower() == preferred_category.lower()
            ]
        
        if not available_scenarios:
            available_scenarios = enhanced_env.scenarios  # Fallback
        
        # Select random scenario
        import random
        selected_scenario = random.choice(available_scenarios)
        enhanced_env.current_scenario = selected_scenario
        
        # Reset environment
        state, source_id = enhanced_env.reset()
        
        # Store session data
        current_session = {
            'scenario': selected_scenario,
            'state': state.tolist(),
            'source_id': source_id,
            'step': 0,
            'total_reward': 0,
            'actions_taken': [],
            'completed': False
        }
        
        return jsonify({
            'success': True,
            'scenario': {
                'title': selected_scenario.get('title', 'Fire Response Scenario'),
                'source': selected_scenario.get('source', 'unknown'),
                'category': selected_scenario.get('category', 'unknown'),
                'situation': selected_scenario.get('situation', ''),
                'difficulty': selected_scenario.get('difficulty', 'medium')
            },
            'session_id': 'enhanced_session_1',
            'available_actions': list(range(enhanced_env.action_dim)),
            'sources_available': list(enhanced_env.source_map.keys())
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/enhanced/get_recommendation', methods=['POST'])
def get_enhanced_recommendation():
    """Get AI recommendation for current scenario state"""
    
    if not current_session or not enhanced_agent:
        return jsonify({'error': 'No active session'}), 400
    
    try:
        # Get current state
        state = np.array(current_session['state'])
        source_id = current_session['source_id']
        
        # Get agent recommendation
        recommended_action = enhanced_agent.select_action(state, source_id)
        
        # Get action confidence (based on Q-values if available)
        confidence = 0.8  # Default confidence
        
        return jsonify({
            'recommended_action': int(recommended_action),
            'confidence': confidence,
            'reasoning': f"Based on enhanced DQN training from multiple sources",
            'source_context': list(enhanced_env.source_map.keys())[source_id]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/enhanced/take_action', methods=['POST'])
def take_enhanced_action():
    """Take an action in the enhanced environment"""
    
    if not current_session or not enhanced_env:
        return jsonify({'error': 'No active session'}), 400
    
    try:
        data = request.get_json()
        action = data.get('action')
        
        if action is None:
            return jsonify({'error': 'Action required'}), 400
        
        # Get current state
        state = np.array(current_session['state'])
        source_id = current_session['source_id']
        
        # Take action in environment
        next_state, reward, done, info = enhanced_env.step(action, source_id)
        
        # Update session
        current_session['state'] = next_state.tolist()
        current_session['step'] += 1
        current_session['total_reward'] += reward
        current_session['actions_taken'].append(action)
        current_session['completed'] = done
        
        # Prepare response
        response = {
            'reward': float(reward),
            'done': done,
            'step': current_session['step'],
            'total_reward': current_session['total_reward'],
            'feedback': info.get('feedback', 'Action completed'),
            'next_state': next_state.tolist()
        }
        
        # Add completion summary if done
        if done:
            response['summary'] = {
                'total_steps': current_session['step'],
                'final_reward': current_session['total_reward'],
                'performance_rating': get_performance_rating(
                    current_session['total_reward']
                ),
                'scenario_source': current_session['scenario'].get('source'),
                'scenario_category': current_session['scenario'].get('category')
            }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/enhanced/get_scenario_library', methods=['GET'])
def get_scenario_library():
    """Get information about available scenarios"""
    
    if not enhanced_env:
        return jsonify({'error': 'Enhanced system not initialized'}), 500
    
    try:
        # Organize scenarios by source and category
        library = {
            'total_scenarios': len(enhanced_env.scenarios),
            'sources': {},
            'categories': {},
            'sample_scenarios': []
        }
        
        # Group by source
        for scenario in enhanced_env.scenarios:
            source = scenario.get('source', 'unknown')
            category = scenario.get('category', 'unknown')
            
            if source not in library['sources']:
                library['sources'][source] = 0
            library['sources'][source] += 1
            
            if category not in library['categories']:
                library['categories'][category] = 0
            library['categories'][category] += 1
        
        # Add sample scenarios (first 5)
        for scenario in enhanced_env.scenarios[:5]:
            library['sample_scenarios'].append({
                'title': scenario.get('title', 'Untitled'),
                'source': scenario.get('source', 'unknown'),
                'category': scenario.get('category', 'unknown'),
                'difficulty': scenario.get('difficulty', 'medium'),
                'situation': scenario.get('situation', '')[:200] + '...'
            })
        
        return jsonify(library)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_performance_rating(total_reward):
    """Convert total reward to performance rating"""
    if total_reward >= 20:
        return "Excellent"
    elif total_reward >= 10:
        return "Good"
    elif total_reward >= 0:
        return "Satisfactory"
    else:
        return "Needs Improvement"

@app.route('/api/enhanced/status', methods=['GET'])
def get_enhanced_status():
    """Get status of enhanced system"""
    
    status = {
        'enhanced_system_available': enhanced_env is not None,
        'agent_trained': False,
        'scenarios_loaded': 0,
        'sources_available': [],
        'active_session': current_session.get('scenario', {}).get('title') if current_session else None
    }
    
    if enhanced_env:
        status['scenarios_loaded'] = len(enhanced_env.scenarios)
        status['sources_available'] = list(enhanced_env.source_map.keys())
    
    # Check if agent is trained
    model_path = Path(__file__).parent / "models" / "enhanced_dqn_final.pth"
    status['agent_trained'] = model_path.exists()
    
    return jsonify(status)

if __name__ == '__main__':
    print("🔥 Enhanced Fire Response Training Web API")
    print("=" * 50)
    
    # Initialize enhanced system
    if initialize_enhanced_system():
        print("✅ Enhanced system ready")
        print(f"📚 Scenarios loaded: {len(enhanced_env.scenarios)}")
        print(f"🎯 Training sources: {list(enhanced_env.source_map.keys())}")
        print("🚀 Starting web server...")
        app.run(debug=True, port=5001)
    else:
        print("❌ Failed to start enhanced system")
        print("💡 Try running train_enhanced_dqn.py first")
