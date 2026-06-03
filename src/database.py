# --- src/database.py (Cleaned & updated) ---

import sqlite3
from typing import Any, Tuple

DB_PATH = "data/oncana_chatbot.db"


def get_connection():
    return sqlite3.connect(DB_PATH, timeout=10)


def create_tables():
    with get_connection() as conn:
        cursor = conn.cursor()
        with open("sql/schema.sql", "r") as f:
            schema_sql = f.read()
        cursor.executescript(schema_sql)
        conn.commit()


def insert_log(message_data: Tuple[Any, ...]):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO conversation_logs (
                message_id, conversation_id, user_id, role, message_text, related_topic_id, prompt_used
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, message_data)
        conn.commit()


def insert_summary(summary_data: Tuple[Any, ...]):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO conversation_summaries (
                conversation_id, user_id, key_topics, key_recommendations, contacts_provided, summary_text
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, summary_data)
        conn.commit()


def fetch_cumulative_summary(user_id: str) -> Any:
    """ Dynamically merge all summaries for the user """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT key_topics, key_recommendations, contacts_provided, summary_text
            FROM conversation_summaries
            WHERE user_id = ?
        """, (user_id,))
        rows = cursor.fetchall()

        if not rows:
            return None

        topics = set()
        recommendations = set()
        contacts = set()
        summaries = []

        for row in rows:
            t, r, c, s = row
            if t:
                topics.update([i.strip() for i in t.split(',')])
            if r:
                recommendations.update([i.strip() for i in r.split(',')])
            if c:
                contacts.update([i.strip() for i in c.split(',')])
            if s:
                summaries.append(s)

        return (
            ', '.join(topics),
            ', '.join(recommendations),
            ', '.join(contacts),
            ' '.join(summaries)
        )


def fetch_prompt(prompt_key: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT prompt, model, temperature, top_p, max_output_tokens
            FROM prompts
            WHERE prompt_key = ?
        """, (prompt_key,))
        return cursor.fetchone()


def fetch_user_info(user_id: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, password FROM users
            WHERE user_id = ?
        """, (user_id,))
        return cursor.fetchone()


def fetch_user_profile(user_id: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, age, cancer_type, treatment_history
            FROM users
            WHERE user_id = ?
        """, (user_id,))
        return cursor.fetchone()


def fetch_recent_logs(user_id: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT message_text FROM conversation_logs
            WHERE user_id = ?
            ORDER BY timestamp DESC LIMIT 5
        """, (user_id,))
        return cursor.fetchall()


def fetch_topic_keywords():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT topic_id, keywords FROM topics
        """)
        return cursor.fetchall()
