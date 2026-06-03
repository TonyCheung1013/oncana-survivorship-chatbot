# --- Updated app.py to support full login with user_id ---

from flask import Flask, jsonify, request, render_template, session
from flask_cors import CORS
import uuid
from src import chatbot
from src import database

app = Flask(
    __name__,
    static_folder="../web/static",
    template_folder="../web/templates"
)
app.secret_key = 'oncana-secret-key'  # For session handling
CORS(app)

chatbot = chatbot.CancerChatbot()
EXCLUDED_TABLES = ['prompts']

# === ROUTES ===

@app.route('/')
def landing():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/register')
def register_page():
    return render_template('register.html')


# === LOGIN ROUTES ===

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = data.get("user_id")
    password = data.get("password")

    user_info = database.fetch_user_info(user_id)
    if not user_info:
        return jsonify({"success": False, "message": "User ID not found."})

    name, real_password = user_info
    if password != real_password:
        return jsonify({"success": False, "message": "Incorrect password."})

    return jsonify({"success": True, "user_id": user_id, "name": name})

# === CHATBOT API ===

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message')
    conversation_id = data.get('conversation_id')
    user_id = data.get('user_id')

    try:
        short_part, remaining, _ = chatbot.generate_response(user_input, user_id=user_id, conversation_id=conversation_id)
        return jsonify({'short_part': short_part, 'remaining': remaining})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@app.route('/api/end_session', methods=['POST'])
def end_session():
    data = request.get_json()
    conversation_id = data.get('conversation_id')
    user_id = data.get('user_id')
    if conversation_id and user_id and user_id != 'guest':
        chatbot.end_session(conversation_id, user_id)
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Invalid session'}), 400


# === ADMIN DATA API ===

@app.route('/api/get_data/<table>', methods=['GET'])
def get_data(table):
    if table in EXCLUDED_TABLES:
        return jsonify({'error': 'Access denied to this table'}), 403
    try:
        with database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table}")
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            data = [dict(zip(columns, row)) for row in rows]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete_data/<table>/<record_id>', methods=['DELETE'])
def delete_data(table, record_id):
    if table in EXCLUDED_TABLES:
        return jsonify({'error': 'Access denied to this table'}), 403

    id_column = "user_id" if table == "users" else "conversation_id" if table.startswith("conversation") else "id"
    if table == "contacts":
        id_column = "contact_id"
    elif table == "topics":
        id_column = "topic_id"
    elif table == "subtopics":
        id_column = "subtopic_id"
    elif table == "resource_contents":
        id_column = "content_id"

    try:
        with database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table} WHERE {id_column} = ?", (record_id,))
            conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/add_data/<table>', methods=['POST'])
def add_data(table):
    if table in EXCLUDED_TABLES:
        return jsonify({'error': 'Access denied to this table'}), 403

    data = request.json
    keys = ', '.join(data.keys())
    placeholders = ', '.join(['?'] * len(data))
    values = tuple(data.values())

    try:
        with database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {table} ({keys}) VALUES ({placeholders})", values)
            conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/update_data/<table>/<record_id>', methods=['PUT'])
def update_data(table, record_id):
    if table in EXCLUDED_TABLES:
        return jsonify({'error': 'Access denied to this table'}), 403

    data = request.json
    columns = ', '.join([f"{key} = ?" for key in data.keys()])
    values = tuple(data.values())

    id_column = "user_id" if table == "users" else "conversation_id" if table.startswith("conversation") else "id"
    if table == "contacts":
        id_column = "contact_id"
    elif table == "topics":
        id_column = "topic_id"
    elif table == "subtopics":
        id_column = "subtopic_id"
    elif table == "resource_contents":
        id_column = "content_id"

    try:
        with database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE {table} SET {columns} WHERE {id_column} = ?", (*values, record_id))
            conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# === REGISTRATION API ===

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    user_id = data.get('user_id')
    name = data.get('name')
    password = data.get('password')
    age = data.get('age')
    cancer_type = data.get('cancer_type')
    treatment_history = data.get('treatment_history')

    # Check for blanks
    if not all([user_id, name, password, age, cancer_type, treatment_history]):
        return jsonify({'success': False, 'message': 'Please fill in all fields.'}), 400

    try:
        with database.get_connection() as conn:
            cursor = conn.cursor()
            # Check duplicate
            cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
            if cursor.fetchone():
                return jsonify({'success': False, 'message': 'User ID already exists.'}), 409

            # Insert user
            cursor.execute("""
                INSERT INTO users (user_id, name, password, age, cancer_type, treatment_history)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, name, password, age, cancer_type, treatment_history))
            conn.commit()
        return jsonify({'success': True, 'message': 'Registration successful!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Registration failed: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
