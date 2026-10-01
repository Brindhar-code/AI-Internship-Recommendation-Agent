from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class InternshipRecommendation:
    """
    Standard representation of one internship recommendation.
    """

    title: str = ""
    company: str = ""
    location: str = ""
    skills: str = ""
    duration: str = ""
    description: str = ""

    match_score: float = 0.0

    extra: Dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "skills": self.skills,
            "duration": self.duration,
            "description": self.description,
            "match_score": self.match_score,
            **self.extra
        }


def normalize_recommendation(
    recommendation: Any
) -> Dict[str, Any]:
    """
    Convert different recommendation formats into
    one common dictionary format.
    """

    if isinstance(recommendation, InternshipRecommendation):
        return recommendation.to_dict()

    if isinstance(recommendation, dict):
        return {
            "title": recommendation.get("title", ""),
            "company": recommendation.get("company", ""),
            "location": recommendation.get("location", ""),
            "skills": recommendation.get("skills", ""),
            "duration": recommendation.get("duration", ""),
            "description": recommendation.get("description", ""),
            "match_score": recommendation.get(
                "match_score",
                recommendation.get("score", 0)
            )
        }

    return {
        "title": str(recommendation),
        "company": "",
        "location": "",
        "skills": "",
        "duration": "",
        "description": "",
        "match_score": 0
    }


def normalize_recommendations(
    recommendations: List[Any]
) -> List[Dict[str, Any]]:
    """
    Normalize a complete list of recommendations.
    """

    if not recommendations:
        return []

    return [
        normalize_recommendation(item)
        for item in recommendations
    ]