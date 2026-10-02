Explainability

1. Purpose

The AI Internship Recommendation Agent is designed to provide transparent, resume-driven internship recommendations.

The system does not simply display a random list of internships. It first analyzes the student's uploaded resume, identifies relevant skills, compares those skills with internship requirements, and then produces recommendations based on the resulting relevance.

---

2. Agent Decision Flow

The complete recommendation flow is:

Student Resume
      ↓
PDF Text Extraction
      ↓
Resume Skill Identification
      ↓
Internship Data Retrieval
      ↓
Resume / Internship Text Comparison
      ↓
TF-IDF Feature Representation
      ↓
Cosine Similarity Calculation
      ↓
Internship Relevance
      ↓
Matched Skills + Missing Skills
      ↓
Personalized Recommendations

A recommendation is therefore based on information available from both the student's resume and the internship requirements.

---

3. Input Evidence

The primary evidence used by the agent is:

Student-side evidence

- Uploaded PDF resume
- Extracted resume text
- Skills identified from the resume

Internship-side evidence

- Internship title
- Company
- Location
- Required skills
- Internship description
- Duration

The agent uses these inputs to determine the relevance of an internship to the student's demonstrated skills.

---

4. How Skills Are Identified

The uploaded PDF is processed by the application.

The text extracted from the resume is analyzed to identify relevant technical skills and keywords.

The identified skills become part of the student's skill profile used by the recommendation process.

Important limitation:

A skill not identified from the resume is not proof that the student does not possess that skill. It may simply mean that the skill was not present or was not recognized in the uploaded resume.

---

5. How Recommendations Are Calculated

The project uses TF-IDF and cosine similarity as part of its matching approach.

TF-IDF

TF-IDF represents important terms in the resume and internship information.

Terms that are more informative within the compared text receive greater importance than very common terms.

Cosine Similarity

Cosine similarity measures the similarity between the text representations.

Conceptually:

similarity =
(resume_vector · internship_vector)
/
(||resume_vector|| × ||internship_vector||)

The resulting similarity value is used as a relevance signal for internship matching.

---

6. What the Match Score Means

The match score represents the calculated textual relevance between the available resume information and internship information.

A higher score means that the compared text has greater similarity according to the implemented matching method.

The score should not be interpreted as:

- probability of getting selected
- probability of receiving an interview
- guarantee of internship eligibility
- guarantee of employment

It is a matching signal generated from the available data.

---

7. Recommendation Evidence

For each recommendation, the system can expose information such as:

- Internship title
- Company
- Location
- Required skills
- Match score
- Matched skills
- Missing skills

This information allows the student to inspect the basis of a recommendation instead of receiving only an unexplained result.

---

8. Matched Skills

Matched skills are skills identified from the student's resume that also correspond to skills or requirements associated with an internship.

For example:

Resume skills:
Python, Flask, SQL

Internship requirements:
Python, Flask, Machine Learning

Matched skills:
Python, Flask

The matched skills provide direct evidence for why the internship may be relevant to the student's profile.

---

9. Missing Skills / Skill Gaps

The skill-gap analysis compares the identified student skills with skills required by relevant internships.

For example:

Student skills:
Python, Flask

Internship requirements:
Python, Flask, Machine Learning

Potential skill gap:
Machine Learning

A reported skill gap means that the skill was not identified in the available resume information.

It does not establish that the student has no knowledge of that skill.

---

10. Why a Recommendation Was Generated

The recommendation can be explained through three main factors:

1. Skills identified from the resume.
2. Skills and information associated with the internship.
3. Similarity between the relevant resume and internship text.

Therefore, the student can inspect the recommendation through the displayed match information, matched skills, and missing skills.

---

11. Recommendation Preconditions

The system requires a resume before generating personalized recommendations.

The intended flow is:

No Resume
   ↓
No Personalized Recommendation

Resume Uploaded
   ↓
Resume Analysis
   ↓
Skill Identification
   ↓
Internship Matching
   ↓
Personalized Recommendation

This prevents the application from presenting internship listings as personalized recommendations before analyzing the student's resume.

---

12. Transparency and Limitations

The recommendation system depends on the quality and content of the uploaded resume and the available internship information.

Potential limitations include:

- A poorly formatted resume may reduce useful text extraction.
- Skills not explicitly represented in the resume may not be identified.
- Internship descriptions may contain incomplete information.
- Text similarity does not represent every aspect of a student's abilities.
- The system does not evaluate interviews, communication skills, academic performance, company-specific selection criteria, or other factors unless they are represented in the available data.

Therefore, recommendations are intended as career-assistance suggestions rather than guaranteed outcomes.

---

13. Privacy and Data Processing

The project follows a local-first approach.

Resume processing is performed by the local application rather than requiring the resume to be sent to an external AI service.

The project does not claim external model processing or hardware acceleration unless such deployment has actually been implemented and verified.

---

14. Reproducibility

The recommendation process can be reproduced using:

- The same resume input
- The same internship dataset
- The same skill-identification logic
- The same TF-IDF configuration
- The same cosine-similarity calculation

This provides a traceable basis for understanding how the recommendation was produced.

---

15. Human Interpretation

The final recommendation should be interpreted by the student.

The agent provides evidence and relevance information to assist the student's internship search.

It does not make a guaranteed decision about whether a student will be accepted by an organization.
