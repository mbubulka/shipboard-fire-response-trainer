#!/usr/bin/env python3
"""
DCA Assessment Feedback Collection System
Comprehensive feedback mechanism for continuous learning and model improvement
"""

import json
import sqlite3
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import hashlib


@dataclass
class FeedbackData:
    """Structure for collecting user feedback on DCA assessments"""
    session_id: str
    user_id: str
    scenario_id: str
    scenario_source: str  # nfpa_1500, uscg, navy, etc.
    scenario_category: str  # fire_suppression, emergency_response, etc.
    
    # User actions and performance
    actions_taken: List[int]
    ai_recommendations: List[int]
    user_followed_ai: List[bool]
    response_times: List[float]  # Time taken for each action
    
    # Performance metrics
    final_score: float
    completion_time: float
    errors_made: int
    critical_errors: int
    
    # User feedback
    difficulty_rating: int  # 1-5 scale
    ai_helpfulness: int  # 1-5 scale
    scenario_realism: int  # 1-5 scale
    confidence_level: int  # 1-5 scale
    
    # Qualitative feedback
    what_worked_well: str
    what_was_confusing: str
    suggested_improvements: str
    additional_comments: str
    
    # Expert validation (if available)
    expert_review: Optional[str] = None
    expert_score: Optional[float] = None
    expert_corrections: Optional[List[str]] = None
    
    # Metadata
    training_level: str = "novice"  # novice, intermediate, advanced, expert
    previous_experience: str = "none"
    timestamp: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Create from dictionary"""
        return cls(**data)


class FeedbackDatabase:
    """Database manager for feedback collection and analysis"""
    
    def __init__(self, db_path: str = "dca_feedback.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize the feedback database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Main feedback table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                scenario_id TEXT NOT NULL,
                scenario_source TEXT NOT NULL,
                scenario_category TEXT NOT NULL,
                
                actions_taken TEXT NOT NULL,
                ai_recommendations TEXT NOT NULL,
                user_followed_ai TEXT NOT NULL,
                response_times TEXT NOT NULL,
                
                final_score REAL NOT NULL,
                completion_time REAL NOT NULL,
                errors_made INTEGER NOT NULL,
                critical_errors INTEGER NOT NULL,
                
                difficulty_rating INTEGER NOT NULL,
                ai_helpfulness INTEGER NOT NULL,
                scenario_realism INTEGER NOT NULL,
                confidence_level INTEGER NOT NULL,
                
                what_worked_well TEXT,
                what_was_confusing TEXT,
                suggested_improvements TEXT,
                additional_comments TEXT,
                
                expert_review TEXT,
                expert_score REAL,
                expert_corrections TEXT,
                
                timestamp TEXT NOT NULL,
                training_level TEXT NOT NULL,
                previous_experience TEXT,
                
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Performance analytics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_date TEXT NOT NULL,
                scenario_source TEXT NOT NULL,
                scenario_category TEXT NOT NULL,
                
                total_sessions INTEGER NOT NULL,
                avg_score REAL NOT NULL,
                avg_completion_time REAL NOT NULL,
                avg_errors REAL NOT NULL,
                avg_difficulty_rating REAL NOT NULL,
                avg_ai_helpfulness REAL NOT NULL,
                
                improvement_areas TEXT,
                recommendations TEXT,
                
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Model training queue table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS training_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                feedback_ids TEXT NOT NULL,
                training_type TEXT NOT NULL,
                status TEXT NOT NULL,
                priority INTEGER NOT NULL,
                
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed_at TIMESTAMP,
                results TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def store_feedback(self, feedback: FeedbackData) -> int:
        """Store feedback data in the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO feedback (
                session_id, user_id, scenario_id, scenario_source, scenario_category,
                actions_taken, ai_recommendations, user_followed_ai, response_times,
                final_score, completion_time, errors_made, critical_errors,
                difficulty_rating, ai_helpfulness, scenario_realism, confidence_level,
                what_worked_well, what_was_confusing, suggested_improvements, additional_comments,
                expert_review, expert_score, expert_corrections,
                timestamp, training_level, previous_experience
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            feedback.session_id, feedback.user_id, feedback.scenario_id,
            feedback.scenario_source, feedback.scenario_category,
            json.dumps(feedback.actions_taken),
            json.dumps(feedback.ai_recommendations),
            json.dumps(feedback.user_followed_ai),
            json.dumps(feedback.response_times),
            feedback.final_score, feedback.completion_time,
            feedback.errors_made, feedback.critical_errors,
            feedback.difficulty_rating, feedback.ai_helpfulness,
            feedback.scenario_realism, feedback.confidence_level,
            feedback.what_worked_well, feedback.what_was_confusing,
            feedback.suggested_improvements, feedback.additional_comments,
            feedback.expert_review, feedback.expert_score,
            json.dumps(feedback.expert_corrections) if feedback.expert_corrections else None,
            feedback.timestamp, feedback.training_level, feedback.previous_experience
        ))
        
        feedback_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return feedback_id
    
    def get_recent_feedback(self, days: int = 7) -> List[Dict]:
        """Get recent feedback for analysis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM feedback 
            WHERE created_at >= date('now', '-{} days')
            ORDER BY created_at DESC
        """.format(days))
        
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        
        # Convert to list of dictionaries
        return [dict(zip(columns, row)) for row in results]
    
    def get_performance_by_source(self, source: str) -> Dict:
        """Get performance analytics for a specific training source"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_sessions,
                AVG(final_score) as avg_score,
                AVG(completion_time) as avg_completion_time,
                AVG(errors_made) as avg_errors,
                AVG(difficulty_rating) as avg_difficulty,
                AVG(ai_helpfulness) as avg_ai_helpfulness,
                AVG(scenario_realism) as avg_realism,
                AVG(confidence_level) as avg_confidence
            FROM feedback 
            WHERE scenario_source = ?
        """, (source,))
        
        result = cursor.fetchone()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        
        if result:
            return dict(zip(columns, result))
        return {}


class FeedbackAnalyzer:
    """Analyzes feedback data to identify improvement opportunities"""
    
    def __init__(self, db: FeedbackDatabase):
        self.db = db
    
    def analyze_ai_recommendation_effectiveness(self) -> Dict:
        """Analyze how effective AI recommendations are"""
        recent_feedback = self.db.get_recent_feedback(days=30)
        
        if not recent_feedback:
            return {"error": "No recent feedback data available"}
        
        total_sessions = len(recent_feedback)
        followed_ai_scores = []
        ignored_ai_scores = []
        
        for feedback in recent_feedback:
            actions = json.loads(feedback['actions_taken'])
            ai_recs = json.loads(feedback['ai_recommendations'])
            followed = json.loads(feedback['user_followed_ai'])
            
            # Calculate scores when user followed vs ignored AI
            for i, (action, ai_rec, did_follow) in enumerate(zip(actions, ai_recs, followed)):
                if did_follow:
                    followed_ai_scores.append(feedback['final_score'])
                else:
                    ignored_ai_scores.append(feedback['final_score'])
        
        analysis = {
            'total_sessions': total_sessions,
            'ai_followed_sessions': len(followed_ai_scores),
            'ai_ignored_sessions': len(ignored_ai_scores),
            'avg_score_when_followed': np.mean(followed_ai_scores) if followed_ai_scores else 0,
            'avg_score_when_ignored': np.mean(ignored_ai_scores) if ignored_ai_scores else 0,
            'ai_effectiveness_ratio': 0
        }
        
        if analysis['avg_score_when_ignored'] > 0:
            analysis['ai_effectiveness_ratio'] = (
                analysis['avg_score_when_followed'] / analysis['avg_score_when_ignored']
            )
        
        return analysis
    
    def identify_difficult_scenarios(self, threshold: float = 3.5) -> List[Dict]:
        """Identify scenarios that users find consistently difficult"""
        recent_feedback = self.db.get_recent_feedback(days=30)
        
        scenario_difficulty = {}
        
        for feedback in recent_feedback:
            scenario_key = f"{feedback['scenario_source']}_{feedback['scenario_category']}"
            
            if scenario_key not in scenario_difficulty:
                scenario_difficulty[scenario_key] = {
                    'ratings': [],
                    'scores': [],
                    'errors': [],
                    'completion_times': []
                }
            
            scenario_difficulty[scenario_key]['ratings'].append(feedback['difficulty_rating'])
            scenario_difficulty[scenario_key]['scores'].append(feedback['final_score'])
            scenario_difficulty[scenario_key]['errors'].append(feedback['errors_made'])
            scenario_difficulty[scenario_key]['completion_times'].append(feedback['completion_time'])
        
        difficult_scenarios = []
        
        for scenario, data in scenario_difficulty.items():
            avg_difficulty = np.mean(data['ratings'])
            avg_score = np.mean(data['scores'])
            avg_errors = np.mean(data['errors'])
            
            if avg_difficulty >= threshold or avg_score < 60 or avg_errors > 3:
                difficult_scenarios.append({
                    'scenario': scenario,
                    'avg_difficulty_rating': avg_difficulty,
                    'avg_score': avg_score,
                    'avg_errors': avg_errors,
                    'avg_completion_time': np.mean(data['completion_times']),
                    'session_count': len(data['ratings'])
                })
        
        return sorted(difficult_scenarios, key=lambda x: x['avg_difficulty_rating'], reverse=True)
    
    def generate_improvement_recommendations(self) -> Dict:
        """Generate recommendations for system improvement"""
        ai_effectiveness = self.analyze_ai_recommendation_effectiveness()
        difficult_scenarios = self.identify_difficult_scenarios()
        
        recommendations = {
            'ai_system': [],
            'scenario_content': [],
            'user_interface': [],
            'training_approach': []
        }
        
        # AI system recommendations
        if ai_effectiveness.get('ai_effectiveness_ratio', 0) < 1.1:
            recommendations['ai_system'].append({
                'priority': 'HIGH',
                'issue': 'AI recommendations not significantly improving user performance',
                'suggestion': 'Retrain DQN with recent feedback data focusing on successful user actions',
                'data_needed': 'Last 30 days of user action sequences and outcomes'
            })
        
        # Scenario content recommendations
        for scenario in difficult_scenarios[:3]:  # Top 3 most difficult
            recommendations['scenario_content'].append({
                'priority': 'MEDIUM',
                'issue': f"High difficulty rating for {scenario['scenario']}",
                'suggestion': 'Add more guidance steps or break into smaller sub-scenarios',
                'data_needed': f"User feedback comments for {scenario['scenario']}"
            })
        
        return recommendations


if __name__ == "__main__":
    # Example usage
    print("🔄 DCA Assessment Feedback System")
    print("=" * 50)
    
    # Initialize components
    db = FeedbackDatabase()
    analyzer = FeedbackAnalyzer(db)
    
    print("✅ Feedback system initialized")
    print("📊 Database tables created")
    print("🔍 Analytics engine ready")
    print("\n🎯 System ready to collect and analyze feedback!")
