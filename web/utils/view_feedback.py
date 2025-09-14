#!/usr/bin/env python3
"""
Utility script to view collected feedback
"""
import sqlite3
from pathlib import Path

def view_feedback():
    db_path = Path("dca_feedback.db")
    if not db_path.exists():
        print("❌ No feedback database found")
        return
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("📊 Recent Feedback Entries:")
    cursor.execute("""
        SELECT id, session_id, scenario_id, final_score, 
               difficulty_rating, ai_helpfulness, scenario_realism 
        FROM feedback 
        ORDER BY id DESC 
        LIMIT 5
    """)
    
    rows = cursor.fetchall()
    if not rows:
        print("No feedback entries found")
        return
        
    for row in rows:
        print(f"\nFeedback #{row[0]}")
        print(f"Session: {row[1]}")
        print(f"Scenario: {row[2]}")
        print(f"Score: {row[3]}")
        print(f"Difficulty Rating: {row[4]}/5")
        print(f"AI Helpfulness: {row[5]}/5")
        print(f"Scenario Realism: {row[6]}/5")
        print("-" * 40)

if __name__ == '__main__':
    print("🔍 Viewing Recent Feedback")
    view_feedback()
