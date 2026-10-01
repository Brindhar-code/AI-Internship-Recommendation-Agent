import ai_engine


class ResumeTool:

    def run(self, context):

        resume_text = context.get(
            "resume_text",
            ""
        )

        return ai_engine.analyze_resume(
            resume_text
        )