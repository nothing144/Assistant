"""
Conversation History Manager for JARVIS
Stores and retrieves conversation history for context-aware AI
"""
import sqlite3
import json
from datetime import datetime


class ConversationManager:
    def __init__(self, db_name="jarvis_conversations.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Initialize conversation database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_message TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                session_id TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                started_at TEXT NOT NULL,
                ended_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_conversation(self, user_message, ai_response, session_id=None):
        """Add a conversation to history"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute('''
                INSERT INTO conversations (timestamp, user_message, ai_response, session_id)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, user_message, ai_response, session_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding conversation: {e}")
            return False
    
    def get_recent_conversations(self, limit=10, session_id=None):
        """Get recent conversations for context"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            if session_id:
                cursor.execute('''
                    SELECT timestamp, user_message, ai_response 
                    FROM conversations 
                    WHERE session_id = ?
                    ORDER BY id DESC 
                    LIMIT ?
                ''', (session_id, limit))
            else:
                cursor.execute('''
                    SELECT timestamp, user_message, ai_response 
                    FROM conversations 
                    ORDER BY id DESC 
                    LIMIT ?
                ''', (limit,))
            
            results = cursor.fetchall()
            conn.close()
            
            # Reverse to get chronological order
            conversations = []
            for row in reversed(results):
                conversations.append({
                    "timestamp": row[0],
                    "user": row[1],
                    "ai": row[2]
                })
            
            return conversations
        except Exception as e:
            print(f"Error getting conversations: {e}")
            return []
    
    def get_all_conversations(self):
        """Get all conversations"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, user_message, ai_response 
                FROM conversations 
                ORDER BY id ASC
            ''')
            
            results = cursor.fetchall()
            conn.close()
            
            conversations = []
            for row in results:
                conversations.append({
                    "timestamp": row[0],
                    "user": row[1],
                    "ai": row[2]
                })
            
            return conversations
        except Exception as e:
            print(f"Error getting all conversations: {e}")
            return []
    
    def search_conversations(self, keyword):
        """Search conversations by keyword"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, user_message, ai_response 
                FROM conversations 
                WHERE user_message LIKE ? OR ai_response LIKE ?
                ORDER BY id DESC
            ''', (f'%{keyword}%', f'%{keyword}%'))
            
            results = cursor.fetchall()
            conn.close()
            
            conversations = []
            for row in results:
                conversations.append({
                    "timestamp": row[0],
                    "user": row[1],
                    "ai": row[2]
                })
            
            return conversations
        except Exception as e:
            print(f"Error searching conversations: {e}")
            return []
    
    def clear_old_conversations(self, days=30):
        """Clear conversations older than specified days"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cutoff_date = datetime.now() - timedelta(days=days)
            cutoff_str = cutoff_date.strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute('''
                DELETE FROM conversations 
                WHERE timestamp < ?
            ''', (cutoff_str,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error clearing old conversations: {e}")
            return False
    
    def get_context_string(self, limit=5):
        """Get recent conversation as context string for AI"""
        conversations = self.get_recent_conversations(limit)
        
        if not conversations:
            return ""
        
        context = "Previous conversation context:\n"
        for conv in conversations:
            context += f"User: {conv['user']}\n"
            context += f"Assistant: {conv['ai']}\n"
        
        return context
    
    def clear_all_conversations(self):
        """Clear all conversation history"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM conversations')
            cursor.execute('DELETE FROM sessions')
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error clearing conversations: {e}")
            return False


# Global instance
conversation_manager = ConversationManager()


# Export functions for easy use
def add_conversation(user_msg, ai_response):
    return conversation_manager.add_conversation(user_msg, ai_response)


def get_recent_conversations(limit=10):
    return conversation_manager.get_recent_conversations(limit)


def get_all_conversations():
    return conversation_manager.get_all_conversations()


def get_context_for_ai(limit=5):
    return conversation_manager.get_context_string(limit)


def clear_history():
    return conversation_manager.clear_all_conversations()


from datetime import timedelta
