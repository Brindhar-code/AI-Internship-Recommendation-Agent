from agent.state import AgentState
from tools.resume_tool import ResumeTool


def test_resume_skill_extraction():
    """
    Verify that the ResumeTool can identify skills
    from resume text.
    """

    resume_text = """
    I have experience in Python, Flask, HTML, CSS and SQL.
    I have also worked with Git and GitHub.
    """

    tool = ResumeTool()

    result = tool.run(resume_text)

    skills = result.get("skills", [])

    assert "python" in skills
    assert "flask" in skills
    assert "html" in skills
    assert "css" in skills
    assert "sql" in skills


def test_agent_state():
    """
    Verify that AgentState stores information correctly.
    """

    state = AgentState(
        user_id=1,
        name="Test Student",
        college="Test College",
        department="CSE",
        cgpa="8.5",
        resume_text="Python Flask SQL"
    )

    state.mark_completed("resume_analysis")

    assert state.user_id == 1
    assert state.name == "Test Student"
    assert "resume_analysis" in state.completed_steps


if __name__ == "__main__":

    test_resume_skill_extraction()
    test_agent_state()

    print("All verification tests passed.")