import ai_engine


class SkillGapTool:

    def run(self, context):

        skills = context.get(
            "skills",
            []
        )

        internships = context.get(
            "internships",
            []
        )

        if not skills:
            return []

        if not internships:
            return []

        return ai_engine.skill_gap_analysis(
            skills,
            internships
        )