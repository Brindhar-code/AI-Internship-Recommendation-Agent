# AI Career & Internship Assistant — Snapdragon AI Lab Project

A local-first AI application that analyzes a student's PDF resume, extracts skills,
compares them with internship opportunities and produces explainable internship
recommendations plus a skill-gap report.

## Main idea

The application is intentionally local-first:

1. Resume PDF is uploaded to the local Flask application.
2. Text is extracted locally.
3. Skills are identified locally.
4. TF-IDF + cosine similarity generates internship relevance scores.
5. The dashboard explains matched and missing skills.

This makes the project a useful baseline for an on-device AI demonstration.

## Folder structure

AI_Career_Assistant_Snapdragon/
├── app.py
├── ai_engine.py
├── requirements.txt
├── README.md
├── career_assistant.db   (created automatically)
├── uploads/
├── templates/
│   ├── index.html
│   ├── register.html
│   ├── dashboard.html
│   └── recommendations.html
└── static/
    ├── css/style.css
    └── js/app.js

## Run on Windows

Open the project folder in VS Code.

### 1. Create virtual environment

python -m venv venv

### 2. Activate

venv\Scripts\activate

### 3. Install packages

pip install -r requirements.txt

### 4. Run

python app.py

### 5. Open

http://127.0.0.1:5000

## Snapdragon / Qualcomm AI integration

The project is designed as a local-first baseline. For the final Snapdragon
submission, replace or augment the lightweight recommendation component with a
model deployed through Qualcomm's supported on-device AI stack / QAI AppBuilder
or a Qualcomm AI Hub model that is supported by the target Snapdragon PC.

Do not claim NPU acceleration unless you actually run and verify the model on
the target Snapdragon PC.

## Demo flow

1. Open application.
2. Register with name and email.
3. Open dashboard.
4. Upload a PDF resume.
5. Resume is analyzed locally.
6. Open recommendations.
7. Show match score, matched skills and missing skills.
8. Explain how local inference protects resume data.
9. On Snapdragon hardware, demonstrate the Qualcomm on-device model integration.
