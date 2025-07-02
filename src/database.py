import sqlite3
import json
from datetime import datetime
import os


class Database:
    def __init__(self, db_path="freelancer_app.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_url TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    contact_email TEXT,
                    match_score REAL,
                    email_content TEXT,
                    applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    company TEXT,
                    skills_required TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_data TEXT NOT NULL,
                    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            
    def save_application(self, project, email_content):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO applications 
                (project_url, title, description, contact_email, match_score, 
                 email_content, company, skills_required)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                project['url'],
                project['title'],
                project.get('description', ''),
                project.get('contact_email', ''),
                project.get('match_score', 0.0),
                email_content,
                project.get('company', ''),
                json.dumps(project.get('skills', []))
            ))
            
            conn.commit()
            
    def check_already_applied(self, project_url):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT id FROM applications WHERE project_url = ?', (project_url,))
            return cursor.fetchone() is not None
            
    def get_application_history(self, limit=50):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT title, description, contact_email, email_content, 
                       applied_date, company, match_score
                FROM applications 
                ORDER BY applied_date DESC 
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            
            return [
                {
                    'title': row[0],
                    'description': row[1],
                    'contact_email': row[2],
                    'email_content': row[3],
                    'applied_date': row[4],
                    'company': row[5],
                    'match_score': row[6]
                }
                for row in rows
            ]
            
    def save_user_profile(self, profile_data):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO user_profiles (profile_data)
                VALUES (?)
            ''', (json.dumps(profile_data),))
            
            conn.commit()
            
    def get_latest_profile(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT profile_data FROM user_profiles
                ORDER BY upload_date DESC
                LIMIT 1
            ''')
            
            row = cursor.fetchone()
            if row:
                return json.loads(row[0])
            return None
            
    def get_statistics(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM applications')
            total_applications = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT COUNT(*) FROM applications 
                WHERE applied_date >= date('now', '-7 days')
            ''')
            recent_applications = cursor.fetchone()[0]
            
            cursor.execute('SELECT AVG(match_score) FROM applications')
            avg_match_score = cursor.fetchone()[0] or 0.0
            
            return {
                'total_applications': total_applications,
                'recent_applications': recent_applications,
                'avg_match_score': avg_match_score
            }