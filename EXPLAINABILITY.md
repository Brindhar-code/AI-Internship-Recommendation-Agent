# Explainability Report - AI Internship Recommendation Agent

## 1. Overview
This agent recommends internships to students based on their skills, interests, and academic background. It uses a rule-based + ML hybrid approach to match profiles with internship descriptions.

## 2. Data Sources
- Student profile: skills, education, interests (user input)
- Internship dataset: title, required skills, domain, location
- No personal sensitive data is stored. All processing is in-memory.

## 3. Model / Decision Logic
- Step 1: Preprocess student skills into TF-IDF vectors
- Step 2: Compute cosine similarity between student vector and internship vectors
- Step 3: Rank internships by similarity score (0-1)
- Step 4: Filter by domain match and location preference
- Step 5: Return top 5 recommendations with explanation of why matched

## 4. Explainability Methods
- **Feature Importance:** Shows which skills matched (e.g., "Matched because you have Python, ML")
- **Similarity Score:** Each recommendation includes a score and reasoning
- **Transparent Ranking:** No black-box; ranking is deterministic cosine similarity
- **SHAP-style logic:** We can explain that if skill X removed, score drops by Y%

## 5. Limitations & Bias Mitigation
- Limited to internships in dataset; may not cover all domains
- Bias: If dataset has more IT internships, IT will be recommended more. Mitigated by balancing domains.
- Does not consider GPA or college name to avoid bias
- Human-in-the-loop: User can see reasoning and reject recommendation

## 6. Audit & Transparency
- All recommendations logged with input skills and output scores
- No external API calls; fully reproducible locally
- Code is open source in this repo for inspection

## 7. Ethical Considerations
- No discrimination based on gender, age, or location
- User consent taken before processing profile
- Explainable to non-technical user
