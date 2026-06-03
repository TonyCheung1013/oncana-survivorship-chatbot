# --- src/init_database.py ---

import sqlite3

DB_PATH = "data/oncana_chatbot.db"


def initialize_database():
    with sqlite3.connect(DB_PATH) as conn:
        # Create tables
        with open("sql/schema.sql", "r") as f:
            schema_sql = f.read()
        conn.executescript(schema_sql)

        # Insert sample data
        with open("sql/insert_sample_data.sql", "r") as f:
            sample_data_sql = f.read()
        conn.executescript(sample_data_sql)

        conn.commit()
        print("✅ Database created and sample data inserted successfully!")


if __name__ == "__main__":
    initialize_database()