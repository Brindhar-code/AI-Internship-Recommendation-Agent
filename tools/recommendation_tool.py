import ai_engine


class RecommendationTool:

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

        return ai_engine.recommend_internships(
            skills,
            internships
        )