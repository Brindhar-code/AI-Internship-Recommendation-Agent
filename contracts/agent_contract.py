from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class AgentRequest:
    """
    Standard input received by the Career Agent.
    """

    user_id: Any = None

    name: str = ""
    college: str = ""
    department: str = ""
    cgpa: str = ""

    resume_text: str = ""

    skills: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "college": self.college,
            "department": self.department,
            "cgpa": self.cgpa,
            "resume_text": self.resume_text,
            "skills": self.skills
        }


@dataclass
class AgentResponse:
    """
    Standard output returned by the Career Agent.
    """

    recommendations: List[Dict[str, Any]] = field(
        default_factory=list
    )

    skill_gaps: List[str] = field(
        default_factory=list
    )

    identified_skills: List[str] = field(
        default_factory=list
    )

    errors: List[str] = field(
        default_factory=list
    )

    completed_steps: List[str] = field(
        default_factory=list
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "recommendations": self.recommendations,
            "skill_gaps": self.skill_gaps,
            "identified_skills": self.identified_skills,
            "errors": self.errors,
            "completed_steps": self.completed_steps
        }