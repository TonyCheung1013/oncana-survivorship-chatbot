-- --- sql/insert_sample_data.sql (Updated with prompt keys) ---

-- Insert sample users
INSERT INTO users (user_id, name, password, age, cancer_type, treatment_history) VALUES
('USR_100001', 'Alice', 'pass123', 45, 'Breast Cancer', 'Surgery, Chemotherapy'),
('USR_100002', 'Bob', 'secure456', 60, 'Prostate Cancer', 'Surgery, Radiation');

-- Insert prompts
INSERT INTO prompts (prompt_key, prompt, model, temperature, top_p, max_output_tokens) VALUES
('initial_prompt', 'You are a helpful chatbot providing information and support to cancer survivors. Base your answers on the survivorship care guidelines provided.', 'gemini-2.0-flash-001', 0.2, 0.95, 800),
('recurrence_prompt', 'You are a helpful chatbot providing reassurance to cancer survivors concerned about recurrence. Use information from the survivorship guidelines.', 'gemini-2.0-flash-001', 0.5, 0.80, 800);

-- Insert topics with prompt keys
INSERT INTO topics (topic_id, name, description, keywords) VALUES
('TOP_FATIGUE', 'Fatigue', 'Information related to fatigue after cancer treatment', 'fatigue,tired,exhaustion,low energy'),
('TOP_RECURRENCE', 'Fear of Recurrence', 'Anxiety about cancer returning', 'recurrence,come back,relapse'),
('TOP_LATE_EFFECTS', 'Late Effects', 'Long-term side effects of cancer treatment', 'late effects,long term effects,side effects'),
('TOP_EMOTIONAL', 'Emotional Wellbeing', 'Coping with emotions after treatment', 'emotional,anxiety,stress,depression'),
('TOP_FOLLOWUP', 'Follow-up Care', 'Guidance on survivorship follow-up', 'follow up,check up,monitoring'),
('TOP_EXERCISE', 'Exercise & Lifestyle', 'Exercise and healthy lifestyle recommendations', 'exercise,lifestyle,healthy living,physical activity'),
('TOP_FINANCIAL', 'Practical & Financial', 'Managing money, work and practical issues', 'financial,money,insurance,cost,bill');


-- Insert subtopics
INSERT INTO subtopics (subtopic_id, topic_id, name, description) VALUES
-- Fatigue
('SUB_FATIGUE_CAUSE', 'TOP_FATIGUE', 'Causes', 'Possible causes of fatigue'),
('SUB_FATIGUE_SYMPTOM', 'TOP_FATIGUE', 'Symptoms', 'Signs and symptoms of fatigue'),
('SUB_FATIGUE_MGMT', 'TOP_FATIGUE', 'Management Strategies', 'How to manage fatigue'),
('SUB_FATIGUE_HELP', 'TOP_FATIGUE', 'When to Seek Help', 'When to contact health providers'),
-- Recurrence
('SUB_RECURRENCE_FACTS', 'TOP_RECURRENCE', 'Facts about Recurrence', 'Understanding cancer recurrence risk'),
('SUB_RECURRENCE_COPING', 'TOP_RECURRENCE', 'Coping Strategies', 'Managing fear and anxiety about recurrence'),
-- Late Effects
('SUB_LATE_EFFECTS_INFO', 'TOP_LATE_EFFECTS', 'Common Late Effects', 'Information about long-term effects'),
-- Emotional
('SUB_EMOTIONAL_COPING', 'TOP_EMOTIONAL', 'Coping Tips', 'Ways to manage emotional wellbeing'),
-- Follow-up
('SUB_FOLLOWUP_PLAN', 'TOP_FOLLOWUP', 'Survivorship Plan', 'What to expect in follow-up care'),
-- Exercise
('SUB_EXERCISE_GUIDE', 'TOP_EXERCISE', 'Exercise Recommendations', 'Safe exercise guidelines after cancer'),
-- Financial
('SUB_FINANCIAL_SUPPORT', 'TOP_FINANCIAL', 'Support Services', 'Where to find financial & practical support');

-- Insert resource contents
INSERT INTO resource_contents (content_id, subtopic_id, content_type, content_text, source_document) VALUES
-- Fatigue
('RC_FATIGUE_MGMT_001', 'SUB_FATIGUE_MGMT', 'recommendation', 'Take short naps and rest between activities.', 'ACSC_FactSheet_Fatigue.pdf'),
('RC_FATIGUE_MGMT_002', 'SUB_FATIGUE_MGMT', 'recommendation', 'Engage in light physical activity like walking.', 'COSA_Exercise_Position_Statement.pdf'),
('RC_FATIGUE_MGMT_003', 'SUB_FATIGUE_MGMT', 'recommendation', 'Maintain a balanced diet and stay hydrated.', 'Living-Well-After-Cancer.pdf'),
('RC_FATIGUE_MGMT_004', 'SUB_FATIGUE_MGMT', 'recommendation', 'Keep a fatigue diary to track patterns and triggers.', 'ACSC_FactSheet_Fatigue.pdf'),
('RC_FATIGUE_HELP_001', 'SUB_FATIGUE_HELP', 'alert', 'If fatigue is overwhelming and persistent, contact your healthcare team.', 'ACSC_FactSheet_Fatigue.pdf'),
-- Recurrence
('RC_RECURRENCE_FACT_001', 'SUB_RECURRENCE_FACTS', 'general_info', 'Risk of recurrence varies by cancer type and treatment.', 'ACSC_Factsheet_Fear_of_Cancer_Coming_Back.pdf'),
('RC_RECURRENCE_COPING_001', 'SUB_RECURRENCE_COPING', 'recommendation', 'Join a support group to share feelings and reduce anxiety.', 'ACSC_Factsheet_Fear_of_Cancer_Coming_Back.pdf'),
('RC_RECURRENCE_COPING_002', 'SUB_RECURRENCE_COPING', 'recommendation', 'Practice mindfulness or relaxation techniques.', 'Living-Well-After-Cancer.pdf'),
-- Late Effects
('RC_LATE_EFFECTS_INFO_001', 'SUB_LATE_EFFECTS_INFO', 'general_info', 'Some treatments can cause long-term side effects like heart issues or bone problems.', 'ACSC_Factsheet_Late_Effects.pdf'),
-- Emotional
('RC_EMOTIONAL_COPING_001', 'SUB_EMOTIONAL_COPING', 'tip', 'Talk to someone you trust about your feelings.', 'Living-Well-After-Cancer.pdf'),
('RC_EMOTIONAL_COPING_002', 'SUB_EMOTIONAL_COPING', 'tip', 'Consider speaking with a psychologist or counselor.', 'ACSC_Factsheet_Emotional_Impact.pdf'),
-- Follow-up
('RC_FOLLOWUP_PLAN_001', 'SUB_FOLLOWUP_PLAN', 'general_info', 'Follow-up care includes regular scans and discussions with your care team.', 'Living-Well-After-Cancer.pdf'),
-- Exercise
('RC_EXERCISE_GUIDE_001', 'SUB_EXERCISE_GUIDE', 'recommendation', 'Aim for 150 minutes of moderate exercise per week.', 'COSA_Exercise_Position_Statement.pdf'),
('RC_EXERCISE_GUIDE_002', 'SUB_EXERCISE_GUIDE', 'recommendation', 'Include resistance training twice per week.', 'COSA_Exercise_Position_Statement.pdf'),
-- Financial
('RC_FINANCIAL_SUPPORT_001', 'SUB_FINANCIAL_SUPPORT', 'tip', 'Speak with a social worker about financial support options.', 'ACSC_FactSheet_Dealing_with_Money_Work.pdf');

-- Insert contacts
INSERT INTO contacts (contact_id, subtopic_id, name, phone, email, website) VALUES
('CT_FATIGUE_HELP_01', 'SUB_FATIGUE_HELP', 'Cancer Council Helpline', '13 11 20', 'info@cancer.org.au', 'www.cancer.org.au'),
('CT_RECURRENCE_HELP_01', 'SUB_RECURRENCE_COPING', 'Cancer Connect Peer Support', '1800 123 456', 'support@cancerconnect.org', 'www.cancerconnect.org'),
('CT_FINANCIAL_SUPPORT_01', 'SUB_FINANCIAL_SUPPORT', 'Cancer Council Legal & Financial', '1300 755 632', 'legal@cancer.org.au', 'www.cancer.org.au/legal');
