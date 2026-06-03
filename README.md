# 📘 Project Overview
Oncana Survivorship Chatbot is a conversational AI tool developed to support cancer survivors with ongoing care and lifestyle guidance after treatment. The chatbot offers tailored recommendations, emotional support information, and follow-up care reminders based on survivorship guidelines and individual patient profiles.

This prototype is part of an academic project aimed at demonstrating how AI and structured databases can enhance patient-centered care. It allows both guests and registered users to interact with the chatbot. Registered users receive more personalized responses that consider their cancer type, treatment history, and previous conversation logs.

The chatbot is integrated with Google's Gemini AI (via Vertex AI) to generate informative responses, while the interface is designed to mimic a realistic clinical support tool with a clean, branded UI.

# ✨ Features
The Oncana Survivorship Chatbot prototype includes the following key functionalities:

💬 Conversational Chat Support
Provides survivorship care information based on user input.
Supports progressive disclosure: gives concise answers first, and offers more if requested.

🔑 User Login & Guest Access
Registered users can log in with a unique ID and password.
Guests can chat without login, but without personalized summaries or history.

📂 Admin Panel
View, add, update, or delete data for: Users, Topics, Subtopics, Resource contents, Conversation logs and summaries
Access via http://127.0.0.1:5000/admin.

📝 User Registration Page
Allows new users to register via a styled registration form.
Dropdowns available for cancer type and treatment history.
Validation checks for blank fields and duplicate user IDs.

🧠 Smart Topic Detection
Dynamically detects conversation topics using keyword mapping stored in the database.

📦 Database Logging
Logs every user-bot exchange with associated metadata.
Summarizes each session and maintains a cumulative user history (for registered users).

# 📁 Project Structure
```
oncana-chatbot/
│
├── src/                          # Python backend source files
│   ├── app.py                    # Flask app with routes for chatbot & admin
│   ├── chatbot.py                # Chatbot logic (Gemini integration, progressive disclosure)
│   ├── database.py               # Database access functions (SQLite)
│   ├── conversation_manager.py   # Logging and session summary handler
│
├── data/
│   └── oncana_chatbot.db         # ⚠️ Not included. Run init_database.py to generate.
│
├── sql/
│   └── schema.sql                # Database schema for initializing tables (for development stage only)
│   └── insert_sample_data.sql    # Inserts realistic sample data into tables (for development stage only)
│   └── init_database.py          # Initializes the SQLite database schema (for development stage only)
│
├── web/
│   ├── templates/
│   │   ├── index.html            # Landing page with chatbot UI
│   │   ├── admin.html            # Admin dashboard UI
│   │   └── register.html         # Registration page
│   │
│   ├── static/
│   │   ├── css/
│   │   │   ├── index-style.css   # Landing page styles
│   │   │   ├── admin-style.css   # Admin page styles
│   │   │   └── register-style.css# Registration page styles
│   │   │
│   │   ├── js/
│   │   │   ├── index-script.js   # Landing page behavior (chat logic)
│   │   │   ├── admin-script.js   # Admin interaction
│   │   │   └── register-script.js# Registration form handling
│   │   │
│   │   ├── fonts/                # ⚠️ Not included. Obtain fonts separately.
│   │   └── images/               # ⚠️ Not included. Obtain assets from Oncana.
│
├── .venv/                        # Python virtual environment
├── requirements.txt              # Python dependencies
├── oncana-service-account.json   # ⚠️ NOT included. Add your own credentials file.
└── README.md                     # Project documentation
```

Environment Configuration: 
To run the Oncana Chatbot, you must configure both the local Python environment and connect it with Google Cloud Vertex AI. Follow these steps to prepare the system:

# ✅ Prerequisites

🔐 Authenticate with Google Cloud
Before using the chatbot, you must authenticate your local environment to access Vertex AI. This requires installing the Google Cloud SDK (gcloud CLI).

✅ ☁️ Google Cloud Project & Vertex AI Setup

1. Create a new project on Google Cloud Console:
   - Go to [console.cloud.google.com](https://console.cloud.google.com/)
   - Create a new project (e.g., `oncana-chatbot-project`)

2. Enable Vertex AI API:
   - In the left sidebar, navigate to **APIs & Services > Library**
   - Search for **Vertex AI API**
   - Click **Enable**

3. Create a service account:
   - Go to **IAM & Admin > Service Accounts**
   - Create a new account with `Vertex AI Platform Express Admin` roles
   - Generate a **JSON key**:
      - Click the service account name
      - Go to the "Keys" tab
      - Click the "Add key" dropdown, then select "Create new key"
      - Choose JSON and download the file (this is your credential file)

4. Save and rename the credential file:
   - Move the JSON file into the root of this project
   - Rename it to: oncana-service-account.json
      (You can also replace the existing credential file with your own)

5. Set the following in your code:
   Open `src/chatbot.py` and update these lines to match your actual project details:
   1. Credential Path = "path/to/your/oncana-service-account.json"
      - ⚠ When copying the path, Windows uses \ by default—change it to / manually
   2. project_id = "your-google-cloud-project-id"
   3. location = "your-region-id"  # default should be "us-central1"
      - You can find your region ID on the Vertex AI Dashboard

📌 Note: Ensure your Google Cloud account has billing enabled and sufficient credits to use the Vertex AI API.

✅ Install Google Cloud SDK

1. Download the installer: Google Cloud SDK Installer
2. Run the installer and follow the prompts.
   Right-click the .exe file and choose “Run as administrator”
3. After installation, open your terminal or command prompt and run:
   >> gcloud init
4. This will guide you through authenticating and selecting the project you created earlier.

More details in reference link: https://cloud.google.com/sdk/docs/install?_gl=1*13fvvyy*_up*MQ..&gclid=Cj0KCQjww-HABhCGARIsALLO6XxKg3LaIDdYGGNg8vjx4p4SdEI7H2DfWT_KyzSGdilD8LNm38xdjZwaAsoEEALw_wcB&gclsrc=aw.ds


✅ Python version 3.9+

📦 Set Up Python Environment

You must install Python before creating the virtual environment.
Download the latest version from: https://www.python.org/downloads/

After Python is installed:
1. Open VSCode
2. Press Ctrl + Shift + P, then select "Python: Create Environment"
3. Once the environment is created, open the integrated terminal and run:
   >> pip install --upgrade google-genai
   >> pip install -r requirements.txt

⚠️ If you encounter an error related to from google.genai import types in chatbot.py, it might be due to incorrect installation paths.
To resolve this:
1. Ensure you're installing packages into the .venv directory in your project.
2. Activate the virtual environment using PowerShell:
   >> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   >> .\.venv\Scripts\Activate
3. Then reinstall the packages:
   >> pip install --upgrade google-genai
   >> pip install -r requirements.txt

✔ This should install the packages in the correct .venv folder and fix any import errors.

# 🚀 Start the Application

Once your environment is configured and the database is initialized, you can launch the Oncana chatbot prototype using the built-in Flask development server.

In the terminal, navigate to the root of the project and run:
   >> python -m src.app

This will start the Flask web server on:
http://127.0.0.1:5000/
http://127.0.0.1:5000/admin
http://127.0.0.1:5000/register


# 🚧 Known Limitations
1. Not a Medical Device
Oncana chatbot is not intended to provide clinical diagnoses or treatment plans. It offers general survivorship care support only.
2. Typo Handling
While some basic typo detection exists, advanced NLP correction is not fully implemented.
3. Model Limitations
Responses are subject to the constraints of Google’s Gemini API (token limits, model behavior, etc.).
4. Static Dataset
Recommendations and responses rely on a fixed dataset of survivorship guidelines; continuous updating is manual.


# 🙏 Acknowledgments
- Gemini / Vertex AI – Language model API provided by Google Cloud
- Oncana Design System – Fonts and branding assets from Oncana's internal design library
- Queensland University of Technology (QUT) – Project developed as part of IFN711 IT Industry Project
- Team Members & Supervisors – Special thanks to our academic supervisors and project stakeholders

# 📄 License
This project is developed for academic and prototyping purposes only.
No part of the chatbot should be considered as medical advice or commercially deployed software.
All rights reserved by the original developers and project stakeholders.
