AI Internship Recommendation Agent

An AI-powered internship recommendation system that analyzes a student's resume, extracts relevant skills, matches them with available internship opportunities, and identifies skill gaps for career development.

🎯 Project Overview

The AI Internship Recommendation Agent is designed to help students discover internship opportunities that match their skills and resume.

The system analyzes the uploaded resume and uses intelligent matching techniques to generate personalized internship recommendations instead of displaying random internship listings.

How it works

1. Student registers and logs into the application.
2. Student uploads a PDF resume.
3. The system extracts the resume text locally.
4. Relevant skills are identified from the resume.
5. Internship opportunities are compared with the student's skills.
6. Matching scores are generated.
7. The system displays suitable internship recommendations.
8. Missing or required skills are identified through skill-gap analysis.

✨ Key Features

- 📄 PDF Resume Upload
- 🤖 AI-based Resume Analysis
- 🔍 Skill Extraction
- 🎯 Personalized Internship Recommendations
- 📊 Internship Match Scoring
- 🧩 Skill Gap Analysis
- 👤 Student Profile Management
- 🔐 User Registration and Login
- 🛠️ Internship Management
- 🖥️ Web-based Dashboard
- 💻 Local-first processing

🧠 AI Recommendation Approach

The recommendation system uses text-processing techniques to compare the student's resume with internship requirements.

Matching process

Resume → Text Extraction → Skill Identification → Internship Comparison → Similarity Score → Recommendations

The system uses TF-IDF and cosine similarity as part of the recommendation process to measure the relevance between the student's profile/resume and internship information.

The recommendation result can include:

- Internship title
- Company
- Location
- Required skills
- Match score
- Matched skills
- Missing skills

🏗️ Project Architecture

AI-Internship-Recommendation-Agent/
│
├── app.py
├── ai_engine.py
├── database.py
├── requirements.txt
├── README.MD
├── .gitignore
│
├── agent/
│   ├── __init__.py
│   ├── career_agent.py
│   └── state.py
│
├── adapters/
│   ├── __init__.py
│   └── carrer_agent_adapter.py
│
├── contracts/
│   ├── __init__.py
│   ├── agent_contract.py
│   └── recommendation_contract.py
│
├── tools/
│   ├── __init__.py
│   ├── internship_tool.py
│   ├── recommendation_tool.py
│   ├── resume_tool.py
│   └── skill_gap_tool.py
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── resume.html
│   ├── recommendations.html
│   ├── admin.html
│   ├── edit.html
│   └── students.html
│
├── static/
│   └── css/
│       └── style.css
│
└── verfication/
    ├── __init__.py
    └── test_agent.py

🛠️ Technologies Used

- Python
- Flask
- HTML5
- CSS3
- SQLite
- PyPDF2
- Scikit-learn
- TF-IDF
- Cosine Similarity
- Git & GitHub

🚀 Running the Project

1. Clone the repository

git clone https://github.com/Brindhar-code/AI-Internship-Recommendation-Agent.git

2. Open the project

cd AI-Internship-Recommendation-Agent

3. Create a virtual environment

python -m venv venv

4. Activate the virtual environment

On Windows:

venv\Scripts\activate

5. Install dependencies

pip install -r requirements.txt

6. Run the application

python app.py

7. Open the application

Open your browser and visit:

http://127.0.0.1:5000

🔄 Demo Flow

Register
   ↓
Login
   ↓
Student Profile
   ↓
Upload Resume
   ↓
Resume Analysis
   ↓
Skill Extraction
   ↓
Internship Matching
   ↓
Recommendations
   ↓
Skill Gap Analysis

🔐 Privacy & Local Processing

The project follows a local-first approach for resume processing.

Resume data is processed by the local application rather than requiring the resume to be sent to an external AI service.

This makes the project suitable for demonstrating privacy-aware career assistance and local AI processing.

📱 Snapdragon / On-Device AI

The project was developed with a local-first AI architecture suitable for exploring on-device AI deployment.

For Snapdragon-based deployment, the recommendation or AI components can be further optimized and integrated with supported Qualcomm on-device AI technologies.

Note: NPU acceleration should only be claimed after the model has actually been deployed and verified on compatible Snapdragon hardware.

🔮 Future Enhancements

- Advanced semantic resume matching
- More internship sources
- Real-time internship updates
- Improved skill extraction using NLP
- Personalized learning recommendations
- On-device AI model optimization
- Snapdragon NPU acceleration
- Internship application tracking
- Multilingual student support

👩‍💻 Project

AI Internship Recommendation Agent

Developed as an AI-focused career assistance project with a local-first architecture for personalized internship discovery.

📄 License

This project currently does not include a license.