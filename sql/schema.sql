-- --- sql/schema.sql (Cleaned without cumulative table) ---

CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    age INTEGER,
    cancer_type TEXT,
    treatment_history TEXT
);

CREATE TABLE IF NOT EXISTS topics (
    topic_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    keywords TEXT
);

CREATE TABLE IF NOT EXISTS subtopics (
    subtopic_id TEXT PRIMARY KEY,
    topic_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
);

CREATE TABLE IF NOT EXISTS resource_contents (
    content_id TEXT PRIMARY KEY,
    subtopic_id TEXT NOT NULL,
    content_type TEXT CHECK (content_type IN ('recommendation', 'alert', 'tip', 'general_info', 'practical_advice')),
    content_text TEXT NOT NULL,
    source_document TEXT,
    FOREIGN KEY (subtopic_id) REFERENCES subtopics(subtopic_id)
);

CREATE TABLE IF NOT EXISTS contacts (
    contact_id TEXT PRIMARY KEY,
    subtopic_id TEXT NOT NULL,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    website TEXT,
    FOREIGN KEY (subtopic_id) REFERENCES subtopics(subtopic_id)
);

CREATE TABLE IF NOT EXISTS prompts (
    prompt_key TEXT PRIMARY KEY,
    prompt TEXT NOT NULL,
    model TEXT,
    temperature REAL,
    top_p REAL,
    max_output_tokens INTEGER
);

CREATE TABLE IF NOT EXISTS conversation_logs (
    message_id TEXT PRIMARY KEY,
    conversation_id TEXT,
    user_id TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role TEXT CHECK(role IN ('user', 'bot')),
    message_text TEXT,
    related_topic_id TEXT,
    prompt_used TEXT
);

CREATE TABLE IF NOT EXISTS conversation_summaries (
    conversation_id TEXT PRIMARY KEY,
    user_id TEXT,
    key_topics TEXT,
    key_recommendations TEXT,
    contacts_provided TEXT,
    summary_text TEXT
);
