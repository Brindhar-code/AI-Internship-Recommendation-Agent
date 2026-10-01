import re
from collections import Counter


# =========================================================
# SUPPORTED SKILLS
# =========================================================

SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "javascript",
    "html",
    "css",
    "flask",
    "django",
    "sql",
    "mysql",
    "mongodb",
    "git",
    "github",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "data analysis",
    "pandas",
    "numpy",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "cybersecurity",
    "networking",
    "linux",
    "iot",
    "arduino",
    "react",
    "node.js",
    "node",
    "rest api",
    "api",
    "cloud",
    "cloud computing",
    "aws",
    "azure",
    "docker",
    "oop",
    "communication",
    "problem solving",
    "web development"
]


# =========================================================
# NORMALIZE TEXT
# =========================================================

def normalize(text):

    if not text:
        return ""

    text = str(text).lower()

    text = re.sub(
        r"[^a-z0-9+#.\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# ANALYZE RESUME
# =========================================================

def analyze_resume(text):

    original_text = text or ""
    normalized_text = normalize(original_text)

    detected = []

    for skill in SKILLS:

        skill_normalized = normalize(skill)

        # Special handling for C++
        if skill == "c++":

            if (
                "c++" in original_text.lower()
                or "cplusplus" in original_text.lower()
            ):
                detected.append(skill)

            continue

        # Special handling for C
        if skill == "c":

            pattern = r"(?<![a-z])c(?![a-z])"

            if re.search(
                pattern,
                normalized_text
            ):
                detected.append(skill)

            continue

        # Normal matching
        pattern = (
            r"(?<!\w)"
            + re.escape(skill_normalized)
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            normalized_text
        ):
            detected.append(skill)

    detected = sorted(set(detected))

    return {
        "skills": detected,
        "text_length": len(original_text)
    }


# =========================================================
# INTERNSHIP TEXT
# =========================================================

def internship_text(item):

    return " ".join([
        str(item.get("title", "")),
        str(item.get("company", "")),
        str(item.get("description", "")),
        str(item.get("skills", "")).replace(",", " ")
    ])


# =========================================================
# CALCULATE MATCH SCORE
# =========================================================

def calculate_match_score(
    user_skills,
    internship
):

    user_set = {
        normalize(skill)
        for skill in (user_skills or [])
        if skill
    }

    required_skills = {
        normalize(skill)
        for skill in str(
            internship.get("skills", "")
        ).split(",")
        if skill.strip()
    }

    if not required_skills:

        return 0, [], []

    matched = sorted(
        user_set.intersection(
            required_skills
        )
    )

    missing = sorted(
        required_skills.difference(
            user_set
        )
    )

    overlap = (
        len(matched)
        / len(required_skills)
    )

    # Additional keyword matching
    user_text = " ".join(
        user_skills or []
    ).lower()

    job_text = internship_text(
        internship
    ).lower()

    keyword_matches = 0

    for skill in required_skills:

        if skill in user_text:
            if skill in job_text:
                keyword_matches += 1

    keyword_score = (
        keyword_matches
        / len(required_skills)
    )

    final_score = (
        overlap * 0.75
        +
        keyword_score * 0.25
    )

    final_score = round(
        final_score * 100
    )

    return (
        final_score,
        matched,
        missing
    )


# =========================================================
# RECOMMEND INTERNSHIPS
# =========================================================

def recommend_internships(
    user_skills,
    internships
):

    results = []

    for internship in internships or []:

        score, matched, missing = (
            calculate_match_score(
                user_skills,
                internship
            )
        )

        result = {
            **dict(internship),

            "match_score": score,

            "matched": matched,

            "missing": missing
        }

        results.append(result)

    results.sort(
        key=lambda item:
        item.get("match_score", 0),
        reverse=True
    )

    return results


# =========================================================
# SKILL GAP ANALYSIS
# =========================================================

def skill_gap_analysis(
    user_skills,
    internships
):

    user = {
        normalize(skill)
        for skill in (user_skills or [])
        if skill
    }

    demand = Counter()

    for internship in internships or []:

        required = str(
            internship.get(
                "skills",
                ""
            )
        ).split(",")

        for skill in required:

            skill = normalize(skill)

            if skill and skill not in user:

                demand[skill] += 1

    gaps = []

    for skill, count in demand.most_common(8):

        gaps.append({
            "skill": skill,
            "demand": count
        })

    return gaps