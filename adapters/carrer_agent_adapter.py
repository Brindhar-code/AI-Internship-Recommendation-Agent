from agent.career_agent import CareerAgent
from agent.state import AgentState

from tools.resume_tool import ResumeTool
from tools.internship_tool import InternshipTool
from tools.recommendation_tool import RecommendationTool
from tools.skill_gap_tool import SkillGapTool

from contracts.recommendation_contract import (
    normalize_recommendations
)


class CareerAgentAdapter:
    """
    Flask-facing adapter for the AI Career Agent.

    The Flask application communicates with this adapter
    instead of directly managing the complete Agent workflow.
    """

    def __init__(self):
        self.agent = CareerAgent(
            resume_tool=ResumeTool(),
            internship_tool=InternshipTool(),
            recommendation_tool=RecommendationTool(),
            skill_gap_tool=SkillGapTool()
        )

    def run(
        self,
        user_id=None,
        name="",
        college="",
        department="",
        cgpa="",
        resume_text="",
        skills=None
    ):
        """
        Run the complete Career Agent workflow.
        """

        state = AgentState(
            user_id=user_id,
            name=name or "",
            college=college or "",
            department=department or "",
            cgpa=str(cgpa or ""),
            resume_text=resume_text or "",
            skills=skills or []
        )

        result = self.agent.run(state)

        recommendations = normalize_recommendations(
            result.recommendations
        )

        return {
            "recommendations": recommendations,
            "skill_gaps": result.skill_gaps,
            "identified_skills": result.skills,
            "errors": result.errors,
            "completed_steps": result.completed_steps
        }


def create_career_agent():
    """
    Create and return a CareerAgentAdapter instance.
    """

    return CareerAgentAdapter()