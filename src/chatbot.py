# --- src/chatbot.py (Progressive Disclosure Version) ---

import os
import uuid
from datetime import datetime
from google import genai
from google.genai import types

from src import conversation_manager
from src import database

# === Environment & Gemini Config ===
credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

project_id = "oncana-final"
location = "us-central1"


class CancerChatbot:
    def __init__(self):
        self.client = genai.Client(vertexai=True, project=project_id, location=location)

    def detect_topic_id(self, user_input):
        keywords_data = database.fetch_topic_keywords()
        for topic_id, keywords in keywords_data:
            keyword_list = [k.strip().lower() for k in keywords.split(",")]
            if any(word in user_input.lower() for word in keyword_list):
                return topic_id
        return None

    def split_response(self, response_text):
        """Split long message into short + detailed part"""
        lines = response_text.split("\n")
        short_part = "\n".join(lines[:4]).strip()
        remaining = "\n".join(lines[4:]).strip()
        return short_part, remaining

    def generate_response(self, user_input, user_id=None, conversation_id=None):
        topic_id = self.detect_topic_id(user_input)
        prompt_key = "recurrence_prompt" if topic_id == "TOP_RECURRENCE" else "initial_prompt"
        prompt_data = database.fetch_prompt(prompt_key)
        if not prompt_data:
            raise ValueError(f"Prompt '{prompt_key}' not found in database.")

        prompt_text, model, temperature, top_p, max_tokens = prompt_data

        # Add user profile
        profile_text = ""
        if user_id != "guest":
            profile = database.fetch_user_profile(user_id)
            if profile:
                name, age, cancer_type, treatment_history = profile
                profile_text = f"\n\nUser Profile:\nName: {name}\nAge: {age}\nCancer Type: {cancer_type}\nTreatment History: {treatment_history}"

        # Add summary
        summary_text = ""
        if user_id != "guest":
            cumulative = database.fetch_cumulative_summary(user_id)
            if cumulative:
                topics, recs, contacts, summary = cumulative
                summary_text = f"\n\nPrevious Conversations Summary:\nTopics discussed: {topics}\nRecommendations provided: {recs}\nContacts provided: {contacts}\nSummary: {summary}"

        # Build prompt
        full_prompt = f"{prompt_text}\n\nUser Input: {user_input}{profile_text}{summary_text}"

        contents = [types.Content(role="user", parts=[types.Part.from_text(text=full_prompt)])]
        generate_content_config = types.GenerateContentConfig(
            temperature=temperature or 0.2,
            top_p=top_p or 0.95,
            max_output_tokens=max_tokens or 500,
            response_modalities=["TEXT"]
        )

        response = self.client.models.generate_content(
            model=model or "gemini-2.0-flash-001",
            contents=contents,
            config=generate_content_config
        )

        # Split response
        short_part, remaining = self.split_response(response.text)

        # Log conversation
        if user_id != "guest":
            conversation_manager.log_message(conversation_id, user_id, "user", user_input, topic_id, prompt_key)
            conversation_manager.log_message(conversation_id, user_id, "bot", response.text, topic_id, prompt_key)

        return short_part, remaining, topic_id

    def end_session(self, conversation_id, user_id):
        if user_id == "guest":
            return
        try:
            conversation_manager.store_session_summary(conversation_id, user_id)
            print("✅ Session summary saved.")
        except Exception as e:
            print(f"❗ Error saving summary: {e}")


def login_user():
    while True:
        user_id = input("Enter your user ID (or type 'guest'): ").strip()
        if user_id.lower() == "guest":
            print("\n👋 Welcome, Guest! You can ask general questions.\n")
            return "guest"

        user_info = database.fetch_user_info(user_id)
        if user_info:
            name, password = user_info
            entered_password = input(f"Enter password for {name}: ").strip()
            if entered_password == password:
                print(f"\n✅ Welcome back, {name}!\n")
                return user_id
            else:
                print("❗ Incorrect password. Try again.\n")
        else:
            print("❗ User ID not found. Please try again.\n")


if __name__ == "__main__":
    chatbot = CancerChatbot()
    user_id = login_user()
    conversation_id = str(uuid.uuid4())

    try:
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == "exit":
                chatbot.end_session(conversation_id, user_id)
                print("\n👋 Session ended. Goodbye!")
                break

            short_resp, remaining_resp, topic_id = chatbot.generate_response(user_input, user_id, conversation_id)
            print(f"Chatbot: {short_resp}\n")

            if remaining_resp:
                follow_up = input("Would you like me to provide more details? (yes/no): ").strip().lower()
                if follow_up in ["yes", "y", "more", "continue"]:
                    print(f"\n{remaining_resp}\n")
                else:
                    print("\n👍 Okay! Let me know if you want more information.\n")

    except KeyboardInterrupt:
        chatbot.end_session(conversation_id, user_id)
        print("\n👋 Session ended. Goodbye!")