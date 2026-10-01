from agent.state import AgentState


class CareerAgent:

    def __init__(
        self,
        resume_tool,
        internship_tool,
        recommendation_tool,
        skill_gap_tool
    ):
        self.resume_tool = resume_tool
        self.internship_tool = internship_tool
        self.recommendation_tool = recommendation_tool
        self.skill_gap_tool = skill_gap_tool

    def run(self, state: AgentState):

        # -------------------------------------------------
        # 1. Analyze resume
        # -------------------------------------------------

        resume_result = self.resume_tool.run(
            {
                "resume_text": state.resume_text
            }
        )

        skills = resume_result.get(
            "skills",
            []
        )

        state.skills = skills

        # -------------------------------------------------
        # 2. Get internships
        # -------------------------------------------------

        internships = self.internship_tool.run(
            {
                "internships": state.internships
            }
        )

        # -------------------------------------------------
        # 3. Generate recommendations
        # -------------------------------------------------

        recommendations = self.recommendation_tool.run(
            {
                "skills": skills,
                "internships": internships
            }
        )

        # -------------------------------------------------
        # 4. Find skill gaps
        # -------------------------------------------------

        skill_gaps = self.skill_gap_tool.run(
            {
                "skills": skills,
                "internships": internships
            }
        )

        # -------------------------------------------------
        # 5. Store results
        # -------------------------------------------------

        state.recommendations = recommendations
        state.skill_gaps = skill_gaps

        return state