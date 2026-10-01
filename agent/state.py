class AgentState:

    def __init__(
        self,
        user_id=None,
        name="",
        college="",
        department="",
        cgpa="",
        resume_text="",
        skills=None,
        internships=None,
        recommendations=None,
        skill_gaps=None
    ):
        self.user_id = user_id
        self.name = name
        self.college = college
        self.department = department
        self.cgpa = cgpa
        self.resume_text = resume_text

        self.skills = skills or []
        self.internships = internships or []
        self.recommendations = recommendations or []
        self.skill_gaps = skill_gaps or []

    def to_dict(self):

        return {
            "user_id": self.user_id,
            "name": self.name,
            "college": self.college,
            "department": self.department,
            "cgpa": self.cgpa,
            "resume_text": self.resume_text,
            "skills": self.skills,
            "internships": self.internships,
            "recommendations": self.recommendations,
            "skill_gaps": self.skill_gaps
        }