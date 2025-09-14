#!/usr/bin/env python3
"""
DCA Assessment Feedback Collection System
Collects, analyzes, and processes feedback data for model improvement
"""

import json
import sqlite3
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import hashlib
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DCAFeedbackCollector:
    """Collects and stores DCA assessment feedback data"""
    
    def __init__(self, db_path: str = "dca_feedback.db"):
        self.db_path = Path(db_path)
        self.init_database()
    
    def init_database(self):
        """Initialize the feedback database schema"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Assessment sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS assessment_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    scenario_id TEXT,
                    scenario_source TEXT,
                    scenario_category TEXT,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    completion_status TEXT,
                    final_score REAL,
                    difficulty_level TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Individual actions and decisions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS assessment_actions (
                    action_id TEXT PRIMARY KEY,
                    session_id TEXT,
                    step_number INTEGER,
                    scenario_state TEXT,
                    ai_recommendation INTEGER,
                    ai_confidence REAL,
                    user_action INTEGER,
                    action_timestamp TIMESTAMP,
                    time_taken_seconds REAL,
                    immediate_reward REAL,
                    FOREIGN KEY (session_id) REFERENCES assessment_sessions(session_id)
                )
            """)
            
            # User feedback table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_feedback (
                    feedback_id TEXT PRIMARY KEY,
                    session_id TEXT,
                    action_id TEXT,
                    feedback_type TEXT,
                    feedback_rating INTEGER,
                    feedback_text TEXT,
                    feedback_category TEXT,
                    expert_validation TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES assessment_sessions(session_id),
                    FOREIGN KEY (action_id) REFERENCES assessment_actions(action_id)
                )
            """)
            
            # Model performance metrics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS model_performance (
                    metric_id TEXT PRIMARY KEY,
                    model_version TEXT,
                    evaluation_date TIMESTAMP,
                    scenario_source TEXT,
                    scenario_category TEXT,
                    average_reward REAL,
                    success_rate REAL,
                    user_agreement_rate REAL,
                    expert_approval_rate REAL,
                    total_sessions INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
    
    def log_assessment_session(self, session_data: Dict) -> str:
        """Log a complete assessment session"""
        session_id = self._generate_id(f"session_{datetime.now().isoformat()}")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO assessment_sessions 
                (session_id, user_id, scenario_id, scenario_source, scenario_category,
                 start_time, end_time, completion_status, final_score, difficulty_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_id,
                session_data.get('user_id', 'anonymous'),
                session_data.get('scenario_id'),
                session_data.get('scenario_source'),
                session_data.get('scenario_category'),
                session_data.get('start_time'),
                session_data.get('end_time'),
                session_data.get('completion_status'),
                session_data.get('final_score'),
                session_data.get('difficulty_level')
            ))
            conn.commit()
        
        logger.info(f"Logged assessment session: {session_id}")
        return session_id
    
    def log_assessment_action(self, action_data: Dict) -> str:
        """Log an individual action during assessment"""
        action_id = self._generate_id(f"action_{datetime.now().isoformat()}")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO assessment_actions
                (action_id, session_id, step_number, scenario_state, ai_recommendation,
                 ai_confidence, user_action, action_timestamp, time_taken_seconds, immediate_reward)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                action_id,
                action_data.get('session_id'),
                action_data.get('step_number'),
                json.dumps(action_data.get('scenario_state')),
                action_data.get('ai_recommendation'),
                action_data.get('ai_confidence'),
                action_data.get('user_action'),
                action_data.get('action_timestamp'),
                action_data.get('time_taken_seconds'),
                action_data.get('immediate_reward')
            ))
            conn.commit()
        
        return action_id
    
    def collect_user_feedback(self, feedback_data: Dict) -> str:
        """Collect user feedback on AI recommendations or outcomes"""
        feedback_id = self._generate_id(f"feedback_{datetime.now().isoformat()}")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user_feedback
                (feedback_id, session_id, action_id, feedback_type, feedback_rating,
                 feedback_text, feedback_category, expert_validation)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                feedback_id,
                feedback_data.get('session_id'),
                feedback_data.get('action_id'),
                feedback_data.get('feedback_type'),
                feedback_data.get('feedback_rating'),
                feedback_data.get('feedback_text'),
                feedback_data.get('feedback_category'),
                feedback_data.get('expert_validation')
            ))
            conn.commit()
        
        logger.info(f"Collected user feedback: {feedback_id}")
        return feedback_id
    
    def _generate_id(self, data: str) -> str:
        """Generate a unique ID for database entries"""
        return hashlib.md5(data.encode()).hexdigest()[:16]


class DCAFeedbackAnalyzer:
    """Analyzes collected feedback data for insights and model improvement"""
    
    def __init__(self, db_path: str = "dca_feedback.db"):
        self.db_path = Path(db_path)
    
    def analyze_ai_recommendation_accuracy(self, days_back: int = 30) -> Dict:
        """Analyze how accurate AI recommendations have been"""
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        with sqlite3.connect(self.db_path) as conn:
            query = """
                SELECT 
                    aa.scenario_source,
                    aa.scenario_category,
                    aa.ai_recommendation,
                    aa.user_action,
                    aa.ai_confidence,
                    aa.immediate_reward,
                    uf.feedback_rating,
                    uf.expert_validation
                FROM assessment_actions aa
                JOIN assessment_sessions asess ON aa.session_id = asess.session_id
                LEFT JOIN user_feedback uf ON aa.action_id = uf.action_id
                WHERE asess.created_at >= ?
            """
            
            df = pd.read_sql_query(query, conn, params=[cutoff_date])
        
        if df.empty:
            return {"error": "No data available for analysis"}
        
        analysis = {
            "total_actions": len(df),
            "user_agreement_rate": (df['ai_recommendation'] == df['user_action']).mean(),
            "high_confidence_accuracy": self._calculate_confidence_accuracy(df),
            "source_performance": self._analyze_by_source(df),
            "category_performance": self._analyze_by_category(df),
            "expert_validation_rate": self._calculate_expert_validation(df),
            "recommendation_impact": self._analyze_recommendation_impact(df)
        }
        
        return analysis
    
    def identify_improvement_areas(self) -> Dict:
        """Identify specific areas where the model needs improvement"""
        with sqlite3.connect(self.db_path) as conn:
            # Get scenarios with low performance
            query = """
                SELECT 
                    asess.scenario_source,
                    asess.scenario_category,
                    AVG(asess.final_score) as avg_score,
                    AVG(aa.immediate_reward) as avg_reward,
                    COUNT(*) as session_count,
                    AVG(CASE WHEN aa.ai_recommendation = aa.user_action THEN 1.0 ELSE 0.0 END) as agreement_rate
                FROM assessment_sessions asess
                JOIN assessment_actions aa ON asess.session_id = aa.session_id
                GROUP BY asess.scenario_source, asess.scenario_category
                HAVING session_count >= 5
                ORDER BY avg_score ASC, agreement_rate ASC
            """
            
            df = pd.read_sql_query(query, conn)
        
        if df.empty:
            return {"message": "Insufficient data for improvement analysis"}
        
        # Identify problematic areas
        low_performance = df[df['avg_score'] < df['avg_score'].median()]
        low_agreement = df[df['agreement_rate'] < 0.7]
        
        improvement_areas = {
            "low_scoring_scenarios": low_performance[['scenario_source', 'scenario_category', 'avg_score']].to_dict('records'),
            "low_agreement_scenarios": low_agreement[['scenario_source', 'scenario_category', 'agreement_rate']].to_dict('records'),
            "priority_training_areas": self._prioritize_training_areas(df),
            "feedback_patterns": self._analyze_feedback_patterns()
        }
        
        return improvement_areas
    
    def generate_training_recommendations(self) -> Dict:
        """Generate specific recommendations for model retraining"""
        improvement_areas = self.identify_improvement_areas()
        accuracy_analysis = self.analyze_ai_recommendation_accuracy()
        
        recommendations = {
            "immediate_actions": [],
            "training_data_needs": [],
            "model_adjustments": [],
            "evaluation_metrics": []
        }
        
        # Generate specific recommendations based on analysis
        if accuracy_analysis.get("user_agreement_rate", 0) < 0.8:
            recommendations["immediate_actions"].append({
                "action": "Retrain model with recent feedback data",
                "priority": "high",
                "reason": f"User agreement rate is {accuracy_analysis.get('user_agreement_rate', 0):.2%}"
            })
        
        # Identify sources needing more training data
        source_performance = accuracy_analysis.get("source_performance", {})
        for source, metrics in source_performance.items():
            if metrics.get("accuracy", 0) < 0.75:
                recommendations["training_data_needs"].append({
                    "source": source,
                    "issue": "Low AI recommendation accuracy",
                    "suggested_action": f"Collect more high-quality scenarios from {source}"
                })
        
        return recommendations
    
    def _calculate_confidence_accuracy(self, df: pd.DataFrame) -> Dict:
        """Calculate accuracy for high-confidence recommendations"""
        if df.empty:
            return {}
        
        high_conf = df[df['ai_confidence'] >= 0.8]
        return {
            "high_confidence_actions": len(high_conf),
            "high_confidence_agreement": (high_conf['ai_recommendation'] == high_conf['user_action']).mean() if len(high_conf) > 0 else 0,
            "confidence_correlation": df['ai_confidence'].corr(df['immediate_reward']) if len(df) > 1 else 0
        }
    
    def _analyze_by_source(self, df: pd.DataFrame) -> Dict:
        """Analyze performance by training source"""
        source_analysis = {}
        for source in df['scenario_source'].unique():
            if pd.isna(source):
                continue
            source_data = df[df['scenario_source'] == source]
            source_analysis[source] = {
                "total_actions": len(source_data),
                "accuracy": (source_data['ai_recommendation'] == source_data['user_action']).mean(),
                "avg_reward": source_data['immediate_reward'].mean(),
                "avg_confidence": source_data['ai_confidence'].mean()
            }
        return source_analysis
    
    def _analyze_by_category(self, df: pd.DataFrame) -> Dict:
        """Analyze performance by scenario category"""
        category_analysis = {}
        for category in df['scenario_category'].unique():
            if pd.isna(category):
                continue
            cat_data = df[df['scenario_category'] == category]
            category_analysis[category] = {
                "total_actions": len(cat_data),
                "accuracy": (cat_data['ai_recommendation'] == cat_data['user_action']).mean(),
                "avg_reward": cat_data['immediate_reward'].mean()
            }
        return category_analysis
    
    def _calculate_expert_validation(self, df: pd.DataFrame) -> Dict:
        """Calculate expert validation metrics"""
        expert_data = df[df['expert_validation'].notna()]
        if expert_data.empty:
            return {"expert_validations": 0}
        
        return {
            "expert_validations": len(expert_data),
            "expert_approval_rate": (expert_data['expert_validation'] == 'approved').mean(),
            "expert_feedback_correlation": expert_data['feedback_rating'].corr(expert_data['immediate_reward']) if len(expert_data) > 1 else 0
        }
    
    def _analyze_recommendation_impact(self, df: pd.DataFrame) -> Dict:
        """Analyze the impact of following AI recommendations"""
        followed_recs = df[df['ai_recommendation'] == df['user_action']]
        ignored_recs = df[df['ai_recommendation'] != df['user_action']]
        
        return {
            "followed_recommendations": {
                "count": len(followed_recs),
                "avg_reward": followed_recs['immediate_reward'].mean() if len(followed_recs) > 0 else 0
            },
            "ignored_recommendations": {
                "count": len(ignored_recs),
                "avg_reward": ignored_recs['immediate_reward'].mean() if len(ignored_recs) > 0 else 0
            }
        }
    
    def _prioritize_training_areas(self, df: pd.DataFrame) -> List[Dict]:
        """Prioritize areas needing training based on impact and frequency"""
        # Score based on frequency and performance gap
        df['priority_score'] = df['session_count'] * (1 - df['agreement_rate'])
        
        return df.nlargest(5, 'priority_score')[
            ['scenario_source', 'scenario_category', 'priority_score', 'session_count', 'agreement_rate']
        ].to_dict('records')
    
    def _analyze_feedback_patterns(self) -> Dict:
        """Analyze patterns in user feedback"""
        with sqlite3.connect(self.db_path) as conn:
            feedback_query = """
                SELECT feedback_type, feedback_rating, feedback_category, COUNT(*) as count
                FROM user_feedback
                GROUP BY feedback_type, feedback_rating, feedback_category
            """
            df = pd.read_sql_query(feedback_query, conn)
        
        if df.empty:
            return {"message": "No feedback patterns available"}
        
        return {
            "common_feedback_types": df.groupby('feedback_type')['count'].sum().to_dict(),
            "rating_distribution": df.groupby('feedback_rating')['count'].sum().to_dict(),
            "category_feedback": df.groupby('feedback_category')['count'].sum().to_dict()
        }


class DCAModelRetrainer:
    """Handles retraining of the DQN model using feedback data"""
    
    def __init__(self, feedback_db_path: str = "dca_feedback.db"):
        self.feedback_db_path = Path(feedback_db_path)
        self.analyzer = DCAFeedbackAnalyzer(feedback_db_path)
    
    def prepare_feedback_training_data(self, min_confidence: float = 0.7) -> Optional[List[Dict]]:
        """Prepare training data from user feedback"""
        with sqlite3.connect(self.feedback_db_path) as conn:
            query = """
                SELECT 
                    aa.scenario_state,
                    aa.ai_recommendation,
                    aa.user_action,
                    aa.immediate_reward,
                    aa.ai_confidence,
                    asess.scenario_source,
                    asess.scenario_category,
                    uf.feedback_rating,
                    uf.expert_validation
                FROM assessment_actions aa
                JOIN assessment_sessions asess ON aa.session_id = asess.session_id
                LEFT JOIN user_feedback uf ON aa.action_id = uf.action_id
                WHERE aa.ai_confidence >= ? OR uf.expert_validation = 'approved'
            """
            
            df = pd.read_sql_query(query, conn, params=[min_confidence])
        
        if df.empty:
            logger.warning("No high-quality feedback data available for training")
            return None
        
        # Convert to training examples
        training_data = []
        for _, row in df.iterrows():
            training_example = {
                'state': json.loads(row['scenario_state']),
                'action': row['user_action'],  # Use user action as ground truth
                'reward': self._adjust_reward_based_on_feedback(row),
                'source': row['scenario_source'],
                'category': row['scenario_category'],
                'confidence': row['ai_confidence'],
                'feedback_quality': self._assess_feedback_quality(row)
            }
            training_data.append(training_example)
        
        logger.info(f"Prepared {len(training_data)} training examples from feedback")
        return training_data
    
    def should_retrain_model(self) -> Tuple[bool, Dict]:
        """Determine if model should be retrained based on feedback"""
        analysis = self.analyzer.analyze_ai_recommendation_accuracy(days_back=7)
        
        retrain_triggers = {
            "low_accuracy": analysis.get("user_agreement_rate", 1.0) < 0.75,
            "poor_expert_validation": analysis.get("expert_validation_rate", {}).get("expert_approval_rate", 1.0) < 0.8,
            "insufficient_confidence": analysis.get("high_confidence_accuracy", {}).get("high_confidence_agreement", 1.0) < 0.85,
            "negative_feedback_trend": self._check_feedback_trend()
        }
        
        should_retrain = any(retrain_triggers.values())
        
        return should_retrain, {
            "triggers": retrain_triggers,
            "recommendation": "immediate" if sum(retrain_triggers.values()) >= 2 else "scheduled",
            "analysis_summary": analysis
        }
    
    def generate_retraining_config(self) -> Dict:
        """Generate configuration for model retraining"""
        training_data = self.prepare_feedback_training_data()
        recommendations = self.analyzer.generate_training_recommendations()
        
        config = {
            "training_mode": "feedback_enhanced",
            "feedback_data_available": training_data is not None,
            "feedback_samples": len(training_data) if training_data else 0,
            "focus_areas": recommendations.get("priority_training_areas", []),
            "model_adjustments": {
                "learning_rate": 0.0001,  # Lower for fine-tuning
                "epsilon_start": 0.1,     # Lower exploration
                "batch_size": 64,
                "update_frequency": 5
            },
            "validation_strategy": "expert_feedback_validation",
            "early_stopping": {
                "metric": "user_agreement_rate",
                "threshold": 0.85,
                "patience": 10
            }
        }
        
        return config
    
    def _adjust_reward_based_on_feedback(self, row: pd.Series) -> float:
        """Adjust reward based on user feedback"""
        base_reward = row['immediate_reward']
        
        # Adjust based on feedback rating
        if pd.notna(row['feedback_rating']):
            feedback_multiplier = (row['feedback_rating'] - 3) / 2  # Scale -1 to 1
            base_reward += feedback_multiplier * 0.5
        
        # Boost for expert validation
        if row['expert_validation'] == 'approved':
            base_reward += 1.0
        elif row['expert_validation'] == 'rejected':
            base_reward -= 1.0
        
        return base_reward
    
    def _assess_feedback_quality(self, row: pd.Series) -> str:
        """Assess the quality of feedback data"""
        if row['expert_validation'] == 'approved':
            return "high"
        elif pd.notna(row['feedback_rating']) and row['feedback_rating'] in [1, 5]:
            return "medium"
        elif row['ai_confidence'] >= 0.9:
            return "medium"
        else:
            return "low"
    
    def _check_feedback_trend(self) -> bool:
        """Check if there's a negative trend in recent feedback"""
        with sqlite3.connect(self.feedback_db_path) as conn:
            query = """
                SELECT 
                    DATE(created_at) as feedback_date,
                    AVG(feedback_rating) as avg_rating
                FROM user_feedback
                WHERE created_at >= date('now', '-14 days')
                GROUP BY DATE(created_at)
                ORDER BY feedback_date
            """
            df = pd.read_sql_query(query, conn)
        
        if len(df) < 3:
            return False
        
        # Check if ratings are declining
        recent_trend = df['avg_rating'].tail(3).mean()
        overall_avg = df['avg_rating'].mean()
        
        return recent_trend < overall_avg - 0.5


if __name__ == "__main__":


class DCAModelRetrainer:
    """Retrains the Enhanced DQN model using collected feedback data"""
    
    def __init__(self, model_path: str = "models/enhanced_dqn_final.pth", 
                 feedback_db: str = "dca_feedback.db"):
        self.model_path = Path(model_path)
        self.feedback_db = feedback_db
        self.analyzer = DCAFeedbackAnalyzer(feedback_db)
        
        # Training hyperparameters for retraining
        self.learning_rate = 1e-4  # Lower LR for fine-tuning
        self.batch_size = 16
        self.retrain_episodes = 50  # Shorter retraining cycles
        
    def should_retrain(self, performance_threshold: float = 0.75) -> bool:
        """Determine if model needs retraining based on performance metrics"""
        try:
            analysis = self.analyzer.analyze_model_performance()
            
            # Check overall accuracy
            overall_accuracy = analysis.get('overall_accuracy', 1.0)
            if overall_accuracy < performance_threshold:
                logger.info(f"Retraining triggered: Overall accuracy {overall_accuracy:.3f} below threshold {performance_threshold}")
                return True
            
            # Check for significant user disagreement
            user_agreement = analysis.get('user_agreement_rate', 1.0)
            if user_agreement < 0.6:
                logger.info(f"Retraining triggered: User agreement {user_agreement:.3f} too low")
                return True
            
            # Check recent performance degradation
            if self.analyzer._detect_performance_degradation():
                logger.info("Retraining triggered: Performance degradation detected")
                return True
                
            return False
            
        except Exception as e:
            logger.error(f"Error checking retrain conditions: {e}")
            return False
    
    def prepare_feedback_training_data(self, min_samples: int = 50) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Convert feedback data into training format for DQN"""
        with sqlite3.connect(self.feedback_db) as conn:
            # Get actions with feedback
            query = """
                SELECT 
                    aa.scenario_state,
                    aa.ai_recommendation,
                    aa.user_action,
                    aa.immediate_reward,
                    uf.feedback_rating,
                    uf.expert_validation,
                    asess.scenario_source,
                    asess.scenario_category
                FROM assessment_actions aa
                LEFT JOIN user_feedback uf ON aa.action_id = uf.action_id
                LEFT JOIN assessment_sessions asess ON aa.session_id = asess.session_id
                WHERE aa.scenario_state IS NOT NULL
                ORDER BY aa.action_timestamp DESC
                LIMIT 1000
            """
            
            df = pd.read_sql_query(query, conn)
            
        if len(df) < min_samples:
            logger.warning(f"Insufficient feedback data: {len(df)} samples (minimum {min_samples})")
            return None, None, None
        
        # Process states
        states = []
        targets = []
        weights = []
        
        for _, row in df.iterrows():
            try:
                # Parse state from JSON string
                state = json.loads(row['scenario_state'])
                state_vector = self._state_to_vector(state)
                
                # Calculate improved target based on feedback
                target_q = self._calculate_feedback_target(row)
                
                # Calculate sample weight based on feedback quality
                weight = self._calculate_sample_weight(row)
                
                states.append(state_vector)
                targets.append(target_q)
                weights.append(weight)
                
            except Exception as e:
                logger.warning(f"Error processing feedback sample: {e}")
                continue
        
        if len(states) == 0:
            return None, None, None
            
        return np.array(states), np.array(targets), np.array(weights)
    
    def _state_to_vector(self, state: Dict) -> np.ndarray:
        """Convert state dictionary to vector format expected by DQN"""
        # This should match the state encoding used in enhanced_dqn_system.py
        vector = np.zeros(20)  # Adjust size based on your state space
        
        try:
            # Fire characteristics
            vector[0] = state.get('fire_type', 0)
            vector[1] = state.get('fire_intensity', 0)
            vector[2] = state.get('fire_spread_rate', 0)
            vector[3] = state.get('compartment_size', 0)
            
            # Personnel resources
            vector[4] = state.get('personnel_available', 0)
            vector[5] = state.get('ppe_ready', 0)
            vector[6] = state.get('response_time', 0)
            vector[7] = state.get('crew_training', 0)
            
            # Equipment status
            vector[8] = state.get('hose_availability', 0)
            vector[9] = state.get('foam_system', 0)
            vector[10] = state.get('breathing_apparatus', 0)
            vector[11] = state.get('extinguishers', 0)
            
            # Spatial context
            vector[12] = state.get('compartment_type', 0)
            vector[13] = state.get('adjacent_compartments', 0)
            vector[14] = state.get('ventilation', 0)
            
            # Temporal factors
            vector[15] = state.get('time_since_detection', 0)
            vector[16] = state.get('operational_status', 0)
            
            # Source encoding
            vector[17] = state.get('source_id', 0)
            vector[18] = state.get('scenario_complexity', 0)
            vector[19] = state.get('emergency_level', 0)
            
        except Exception as e:
            logger.warning(f"Error encoding state vector: {e}")
            
        return vector
    
    def _calculate_feedback_target(self, row: pd.Series) -> float:
        """Calculate improved Q-value target based on user feedback"""
        base_reward = row.get('immediate_reward', 0)
        feedback_rating = row.get('feedback_rating', 3)  # Default neutral
        expert_validation = row.get('expert_validation', 'unknown')
        user_action = row.get('user_action', 0)
        ai_recommendation = row.get('ai_recommendation', 0)
        
        # Start with base reward
        target = float(base_reward)
        
        # Adjust based on user feedback rating (1-5 scale)
        if pd.notna(feedback_rating):
            # Convert 1-5 rating to -1 to +1 adjustment
            feedback_adjustment = (feedback_rating - 3) * 0.2
            target += feedback_adjustment
        
        # Expert validation bonus/penalty
        if expert_validation == 'correct':
            target += 0.3
        elif expert_validation == 'incorrect':
            target -= 0.3
        
        # Preference learning: if user chose different action, adjust
        if user_action != ai_recommendation:
            # Slight penalty for AI recommendation, boost for user choice
            target -= 0.1
        
        # Ensure target is in reasonable range
        return np.clip(target, -2.0, 2.0)
    
    def _calculate_sample_weight(self, row: pd.Series) -> float:
        """Calculate importance weight for training sample"""
        weight = 1.0
        
        # Higher weight for samples with explicit feedback
        if pd.notna(row.get('feedback_rating')):
            weight *= 1.5
        
        # Higher weight for expert-validated samples
        if row.get('expert_validation') in ['correct', 'incorrect']:
            weight *= 2.0
        
        # Higher weight for high-stakes scenarios
        if 'hangar' in str(row.get('scenario_category', '')).lower():
            weight *= 1.3
        
        return weight
    
    def retrain_model(self, backup_current: bool = True) -> bool:
        """Retrain the model with feedback data"""
        try:
            # Check if retraining is needed
            if not self.should_retrain():
                logger.info("Retraining not needed - model performance acceptable")
                return False
            
            # Prepare training data
            states, targets, weights = self.prepare_feedback_training_data()
            if states is None:
                logger.warning("Insufficient data for retraining")
                return False
            
            logger.info(f"Starting model retraining with {len(states)} feedback samples")
            
            # Backup current model
            if backup_current and self.model_path.exists():
                backup_path = self.model_path.with_suffix(f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pth')
                import shutil
                shutil.copy2(self.model_path, backup_path)
                logger.info(f"Current model backed up to {backup_path}")
            
            # Load and retrain model
            success = self._perform_retraining(states, targets, weights)
            
            if success:
                # Update model performance tracking
                self._log_retrain_event()
                logger.info("Model retraining completed successfully")
                return True
            else:
                logger.error("Model retraining failed")
                return False
                
        except Exception as e:
            logger.error(f"Error during model retraining: {e}")
            return False
    
    def _perform_retraining(self, states: np.ndarray, targets: np.ndarray, weights: np.ndarray) -> bool:
        """Execute the actual model retraining"""
        try:
            # Import necessary modules
            import torch
            import torch.nn as nn
            import torch.optim as optim
            from enhanced_dqn_system import EnhancedDQN
            
            # Load existing model
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model = EnhancedDQN(state_size=20, action_size=8, num_sources=5)
            
            if self.model_path.exists():
                checkpoint = torch.load(self.model_path, map_location=device)
                model.load_state_dict(checkpoint['model_state_dict'])
                logger.info("Loaded existing model for retraining")
            else:
                logger.warning("No existing model found, training from scratch")
            
            model.to(device)
            model.train()
            
            # Set up optimizer with lower learning rate
            optimizer = optim.Adam(model.parameters(), lr=self.learning_rate)
            criterion = nn.MSELoss(reduction='none')  # No reduction for weighted loss
            
            # Convert to tensors
            states_tensor = torch.FloatTensor(states).to(device)
            targets_tensor = torch.FloatTensor(targets).to(device)
            weights_tensor = torch.FloatTensor(weights).to(device)
            
            # Training loop
            total_loss = 0
            num_batches = 0
            
            for epoch in range(20):  # Multiple passes over feedback data
                # Shuffle data
                indices = torch.randperm(len(states))
                
                for i in range(0, len(indices), self.batch_size):
                    batch_indices = indices[i:i+self.batch_size]
                    
                    batch_states = states_tensor[batch_indices]
                    batch_targets = targets_tensor[batch_indices]
                    batch_weights = weights_tensor[batch_indices]
                    
                    # Forward pass
                    # Assuming source_id is in the state vector
                    source_ids = batch_states[:, 17].long()  # Extract source ID
                    q_values = model(batch_states, source_ids)
                    
                    # For feedback training, we update the Q-value for the action taken
                    # This is a simplified approach - you might want to be more sophisticated
                    predicted_values = q_values.max(dim=1)[0]
                    
                    # Calculate weighted loss
                    loss = criterion(predicted_values, batch_targets)
                    weighted_loss = (loss * batch_weights).mean()
                    
                    # Backward pass
                    optimizer.zero_grad()
                    weighted_loss.backward()
                    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                    optimizer.step()
                    
                    total_loss += weighted_loss.item()
                    num_batches += 1
            
            # Save retrained model
            torch.save({
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'retrain_timestamp': datetime.now().isoformat(),
                'feedback_samples_used': len(states),
                'avg_loss': total_loss / num_batches if num_batches > 0 else 0
            }, self.model_path)
            
            logger.info(f"Model retrained with average loss: {total_loss / num_batches:.4f}")
            return True
            
        except Exception as e:
            logger.error(f"Error in model retraining: {e}")
            return False
    
    def _log_retrain_event(self):
        """Log retraining event to database"""
        try:
            with sqlite3.connect(self.feedback_db) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO model_performance (
                        metric_id, model_version, evaluation_date, 
                        scenario_source, scenario_category, total_sessions
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    hashlib.md5(f"retrain_{datetime.now().isoformat()}".encode()).hexdigest()[:16],
                    "retrained_from_feedback",
                    datetime.now(),
                    "mixed",
                    "retrain_event",
                    0
                ))
                conn.commit()
        except Exception as e:
            logger.warning(f"Could not log retrain event: {e}")
    
    def evaluate_retrained_model(self) -> Dict:
        """Evaluate the retrained model performance"""
        try:
            # Run evaluation using existing evaluation script
            analysis = self.analyzer.analyze_model_performance()
            
            # Add retraining-specific metrics
            retrain_metrics = {
                'retrain_timestamp': datetime.now().isoformat(),
                'model_version': 'retrained_from_feedback',
                'feedback_integration': 'active',
                'continuous_learning': 'enabled'
            }
            
            analysis.update(retrain_metrics)
            return analysis
            
        except Exception as e:
            logger.error(f"Error evaluating retrained model: {e}")
            return {}


if __name__ == "__main__":
    # Example usage
    collector = DCAFeedbackCollector()
    analyzer = DCAFeedbackAnalyzer()
    retrainer = DCAModelRetrainer()
    
    print("🔥 DCA Assessment Feedback System Initialized")
    print("=" * 50)
    print("✅ Feedback collection database ready")
    print("✅ Analysis framework loaded")
    print("✅ Model retraining system available")
    print("\n📋 System ready to collect and analyze DCA assessment feedback!")
