import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path("backups/campaign_memory.db")

class CampaignMemory:
    def __init__(self):
        self._init_db()

    def _init_db(self):
        DB_PATH.parent.mkdir(exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                target_goal TEXT,
                payload TEXT,
                success BOOLEAN,
                model_response TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def log_attempt(self, goal: str, payload: str, success: bool, response: str):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO attacks (timestamp, target_goal, payload, success, model_response)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), goal, payload, success, response))
        conn.commit()
        conn.close()

    def get_successful_payloads(self, goal_keyword: str = None):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query = "SELECT payload FROM attacks WHERE success = 1"
        params = []
        
        if goal_keyword:
            query += " AND target_goal LIKE ?"
            params.append(f"%{goal_keyword}%")
            
        cursor.execute(query, params)
        results = [row[0] for row in cursor.fetchall()]
        conn.close()
        return results
