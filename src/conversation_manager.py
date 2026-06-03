# --- src/conversation_manager.py (Cleaned & Working) ---

import uuid
from datetime import datetime
from src import database


def generate_conversation_id():
    return f"CONV_{uuid.uuid4().hex[:8]}"


def log_message(conversation_id, user_id, role, message_text, related_topic_id=None, prompt_used=None):
    message_id = f"MSG_{uuid.uuid4().hex[:8]}"
    message_data = (
        message_id,
        conversation_id,
        user_id,
        role,
        message_text,
        related_topic_id,
        prompt_used
    )
    database.insert_log(message_data)


def store_session_summary(conversation_id, user_id):
    """ Store session summary into conversation_summaries table """
    with database.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT related_topic_id, message_text
            FROM conversation_logs
            WHERE conversation_id = ? AND role = 'bot'
        """, (conversation_id,))
        logs = cursor.fetchall()

    topics = set()
    recommendations = set()
    contacts = set()
    summary_text = ""

    for topic_id, msg in logs:
        if topic_id:
            topics.add(topic_id)
        if "recommendation" in msg.lower():
            recommendations.add("Some Recommendation")  # Optional: Improve extraction
        if "helpline" in msg.lower() or "contact" in msg.lower():
            contacts.add("Some Contact")
        summary_text += msg + "\n"

    key_topics = ", ".join(topics) if topics else "None"
    key_recs = ", ".join(recommendations) if recommendations else "None"
    key_contacts = ", ".join(contacts) if contacts else "None"

    summary_data = (
        conversation_id,
        user_id,
        key_topics,
        key_recs,
        key_contacts,
        summary_text.strip()
    )

    database.insert_summary(summary_data)


def merge_text(old_text, new_text):
    old_set = set(old_text.split(", ")) if old_text else set()
    new_set = set(new_text.split(", ")) if new_text else set()
    combined = old_set.union(new_set) - {"None"}
    return ", ".join(combined) if combined else "None"
