class InternshipTool:

    def run(self, context):
        """
        Returns the available internships.
        """

        internships = context.get(
            "internships",
            []
        )

        return internships