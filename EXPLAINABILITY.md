Explainability

Overview

The AI Internship Recommendation Agent provides internship recommendations based on the skills identified from a student's uploaded resume.

The recommendation process is designed to be understandable and traceable rather than producing unexplained recommendations.

Recommendation Process

The agent follows these steps:

1. The student uploads a PDF resume.
2. The application extracts the resume text locally.
3. Relevant skills are identified from the extracted resume content.
4. Available internship information is collected from the application's internship database.
5. Resume information and internship requirements are converted into text features.
6. TF-IDF is used to represent the relevant text.
7. Cosine similarity is used to calculate the relevance between the student's profile/resume and internship requirements.
8. Internships with relevant skills are presented as recommendations.
9. The system identifies matched skills and missing skills to explain the recommendation.

Matching Method

The system uses:

- TF-IDF for text feature representation.
- Cosine similarity for measuring text similarity.
- Skill comparison for identifying matched and missing skills.

A higher similarity score indicates greater textual relevance between the student's resume information and the internship requirements.

Recommendation Evidence

Each recommendation can be explained using information such as:

- Internship title
- Company
- Location
- Required skills
- Match score
- Matched skills
- Missing skills

This allows the student to understand why an internship was identified as relevant.

Skill Gap Explainability

The skill-gap component compares the skills identified from the student's resume with skills required by relevant internships.

Skills present in internship requirements but not identified in the resume are reported as missing or potential skill gaps.

Limitations

The recommendation score is based on the available resume text, identified skills, and internship information.

A missing skill in the result does not necessarily mean that the student has no knowledge of that skill; it means that the skill was not identified from the available resume information.

The system does not guarantee internship selection or employment.

Privacy

The project follows a local-first approach for resume processing. Resume information is processed by the local application rather than requiring the resume to be sent to an external AI service.

Transparency

The agent does not claim to use a large language model or NPU acceleration for the recommendation calculation unless those components are actually deployed and verified.
