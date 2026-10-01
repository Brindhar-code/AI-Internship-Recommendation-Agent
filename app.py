from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader

import sqlite3
import os

from agent.career_agent import CareerAgent
from agent.state import AgentState

from tools.resume_tool import ResumeTool
from tools.internship_tool import InternshipTool
from tools.recommendation_tool import RecommendationTool
from tools.skill_gap_tool import SkillGapTool


# =========================================================
# FLASK CONFIGURATION
# =========================================================

app = Flask(__name__)

app.secret_key = "career-ai-demo-secret-key"

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

DATABASE = os.path.join(
    BASE_DIR,
    "internship.db"
)

ALLOWED_EXTENSIONS = {"pdf"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# =========================================================
# AI CAREER AGENT
# =========================================================

career_agent = CareerAgent(
    resume_tool=ResumeTool(),
    internship_tool=InternshipTool(),
    recommendation_tool=RecommendationTool(),
    skill_gap_tool=SkillGapTool()
)


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db():

    connection = sqlite3.connect(
        DATABASE
    )

    connection.row_factory = sqlite3.Row

    return connection


# =========================================================
# CHECK FILE TYPE
# =========================================================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def init_db():

    connection = get_db()

    cursor = connection.cursor()

    # -----------------------------------------------------
    # USERS TABLE
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT NOT NULL UNIQUE,

            skills TEXT DEFAULT '',

            resume_text TEXT DEFAULT '',

            resume_filename TEXT DEFAULT '',

            college TEXT DEFAULT '',

            department TEXT DEFAULT '',

            cgpa TEXT DEFAULT '',

            password TEXT DEFAULT ''
        )
    """)

    # -----------------------------------------------------
    # CHECK EXISTING USER COLUMNS
    # -----------------------------------------------------

    existing_columns = [
        row["name"]
        for row in cursor.execute(
            "PRAGMA table_info(users)"
        ).fetchall()
    ]

    columns_to_add = {
        "college": "TEXT DEFAULT ''",
        "department": "TEXT DEFAULT ''",
        "cgpa": "TEXT DEFAULT ''",
        "password": "TEXT DEFAULT ''"
    }

    for column, definition in columns_to_add.items():

        if column not in existing_columns:

            cursor.execute(
                f"""
                ALTER TABLE users
                ADD COLUMN {column} {definition}
                """
            )

    # -----------------------------------------------------
    # INTERNSHIPS TABLE
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS internships (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            company TEXT NOT NULL,

            location TEXT,

            skills TEXT,

            duration TEXT,

            description TEXT
        )
    """)

    # -----------------------------------------------------
    # ADD SAMPLE INTERNSHIPS
    # -----------------------------------------------------

    cursor.execute(
        "SELECT COUNT(*) FROM internships"
    )

    count = cursor.fetchone()[0]

    if count == 0:

        internships = [

            (
                "Python AI Intern",
                "TechNova Labs",
                "Remote",
                "python,machine learning,flask,sql",
                "2 Months",
                "Work on Python-based AI applications and web systems."
            ),

            (
                "Web Development Intern",
                "WebCraft Solutions",
                "Coimbatore",
                "html,css,javascript,flask,python",
                "1 Month",
                "Develop responsive websites and web applications."
            ),

            (
                "Data Science Intern",
                "DataSphere",
                "Remote",
                "python,pandas,numpy,machine learning,sql",
                "3 Months",
                "Work with data analysis, Python and machine learning."
            ),

            (
                "Cyber Security Intern",
                "SecureNet",
                "Bengaluru",
                "python,networking,linux,cybersecurity",
                "2 Months",
                "Learn practical cybersecurity and networking concepts."
            ),

            (
                "IoT Developer Intern",
                "SmartEdge",
                "Chennai",
                "python,iot,arduino,c",
                "2 Months",
                "Develop IoT applications using Python and embedded systems."
            ),

            (
                "Java Developer Intern",
                "CodeBridge",
                "Hyderabad",
                "java,sql,oop,git",
                "2 Months",
                "Develop Java applications using object-oriented programming."
            )
        ]

        cursor.executemany(
            """
            INSERT INTO internships
            (
                title,
                company,
                location,
                skills,
                duration,
                description
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            internships
        )

    connection.commit()

    connection.close()


# =========================================================
# EXTRACT TEXT FROM PDF
# =========================================================

def extract_pdf_text(pdf_path):

    text = ""

    try:

        reader = PdfReader(
            pdf_path
        )

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"

    except Exception as error:

        print(
            "PDF extraction error:",
            error
        )

    return text.strip()


# =========================================================
# GET CURRENT USER
# =========================================================

def get_current_user():

    user_id = session.get(
        "user_id"
    )

    if not user_id:

        return None

    connection = get_db()

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    connection.close()

    return user


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# =========================================================
# REGISTER
# =========================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

        if not name or not email:

            flash(
                "Please enter your name and email."
            )

            return redirect(
                url_for("register")
            )

        connection = get_db()

        cursor = connection.cursor()

        # -------------------------------------------------
        # CHECK EXISTING USER
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        )

        user = cursor.fetchone()

        if user:

            user_id = user["id"]

            # Update password if it was previously empty
            if password and not user["password"]:

                cursor.execute(
                    """
                    UPDATE users
                    SET
                        name = ?,
                        password = ?
                    WHERE id = ?
                    """,
                    (
                        name,
                        password,
                        user_id
                    )
                )

            else:

                cursor.execute(
                    """
                    UPDATE users
                    SET name = ?
                    WHERE id = ?
                    """,
                    (
                        name,
                        user_id
                    )
                )

        else:

            cursor.execute(
                """
                INSERT INTO users
                (
                    name,
                    email,
                    password
                )
                VALUES (?, ?, ?)
                """,
                (
                    name,
                    email,
                    password
                )
            )

            user_id = cursor.lastrowid

        connection.commit()

        connection.close()

        session["user_id"] = user_id

        session["name"] = name

        flash(
            "Registration successful."
        )

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "register.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

        if not email:

            flash(
                "Please enter your email."
            )

            return redirect(
                url_for("login")
            )

        connection = get_db()

        user = connection.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

        connection.close()

        if not user:

            flash(
                "Account not found. Please register first."
            )

            return redirect(
                url_for("login")
            )

        # -------------------------------------------------
        # Password compatibility
        # -------------------------------------------------

        saved_password = user["password"]

        if saved_password:

            if password != saved_password:

                flash(
                    "Incorrect password."
                )

                return redirect(
                    url_for("login")
                )

        session["user_id"] = user["id"]

        session["name"] = user["name"]

        flash(
            "Login successful."
        )

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "login.html"
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    user_id = session.get(
        "user_id"
    )

    if not user_id:

        return redirect(
            url_for("login")
        )

    connection = get_db()

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    internship_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM internships
        """
    ).fetchone()[0]

    connection.close()

    if not user:

        session.clear()

        return redirect(
            url_for("register")
        )

    user_skills = []

    if user["skills"]:

        user_skills = [
            skill.strip()
            for skill in user["skills"].split(",")
            if skill.strip()
        ]

    return render_template(
        "dashboard.html",
        user=user,
        user_skills=user_skills,
        internship_count=internship_count
    )


# =========================================================
# PROFILE
# =========================================================

@app.route(
    "/profile",
    methods=["GET", "POST"]
)
def profile():

    user_id = session.get(
        "user_id"
    )

    if not user_id:

        return redirect(
            url_for("login")
        )

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        college = request.form.get(
            "college",
            ""
        ).strip()

        department = request.form.get(
            "department",
            ""
        ).strip()

        cgpa = request.form.get(
            "cgpa",
            ""
        ).strip()

        skills = request.form.get(
            "skills",
            ""
        ).strip()

        connection = get_db()

        connection.execute(
            """
            UPDATE users

            SET
                name = ?,
                college = ?,
                department = ?,
                cgpa = ?,
                skills = ?

            WHERE id = ?
            """,
            (
                name,
                college,
                department,
                cgpa,
                skills,
                user_id
            )
        )

        connection.commit()

        connection.close()

        session["name"] = name

        flash(
            "Profile updated successfully."
        )

        return redirect(
            url_for("profile")
        )

    connection = get_db()

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    connection.close()

    if not user:

        session.clear()

        return redirect(
            url_for("register")
        )

    return render_template(
        "profile.html",
        user=user
    )


# =========================================================
# RESUME PAGE
# =========================================================

@app.route("/resume")
def resume():

    user_id = session.get(
        "user_id"
    )

    if not user_id:

        return redirect(
            url_for("login")
        )

    return render_template(
        "resume.html"
    )


# =========================================================
# UPLOAD RESUME
# =========================================================

@app.route(
    "/upload-resume",
    methods=["POST"]
)
def upload_resume():

    user_id = session.get(
        "user_id"
    )

    if not user_id:

        return redirect(
            url_for("login")
        )

    if "resume" not in request.files:

        flash(
            "Please select a resume PDF."
        )

        return redirect(
            url_for("resume")
        )

    file = request.files["resume"]

    if file.filename == "":

        flash(
            "Please select a resume PDF."
        )

        return redirect(
            url_for("resume")
        )

    if not allowed_file(
        file.filename
    ):

        flash(
            "Only PDF resume files are allowed."
        )

        return redirect(
            url_for("resume")
        )

    filename = secure_filename(
        file.filename
    )

    filename = (
        str(user_id)
        + "_"
        + filename
    )

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(file_path)

    # -----------------------------------------------------
    # EXTRACT RESUME TEXT
    # -----------------------------------------------------

    resume_text = extract_pdf_text(
        file_path
    )

    if not resume_text:

        flash(
            "Could not extract text from the PDF. "
            "Please use a PDF containing selectable text."
        )

        return redirect(
            url_for("resume")
        )

    # -----------------------------------------------------
    # GET USER INFORMATION
    # -----------------------------------------------------

    connection = get_db()

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    # -----------------------------------------------------
    # GET ALL INTERNSHIPS
    # -----------------------------------------------------

    internships = connection.execute(
        """
        SELECT *
        FROM internships
        """
    ).fetchall()

    connection.close()

    internship_list = [
        dict(item)
        for item in internships
    ]

    # -----------------------------------------------------
    # CREATE AGENT STATE
    # -----------------------------------------------------

    state = AgentState(

        user_id=user_id,

        name=user["name"] if user else "",

        college=user["college"] if user else "",

        department=user["department"] if user else "",

        cgpa=user["cgpa"] if user else "",

        resume_text=resume_text,

        skills=[]
    )

    # Give internships to the InternshipTool
    state.internships = internship_list

    # -----------------------------------------------------
    # RUN AI CAREER AGENT
    # -----------------------------------------------------

    result = career_agent.run(
        state
    )

    detected_skills = result.skills

    # -----------------------------------------------------
    # SAVE ANALYSIS
    # -----------------------------------------------------

    connection = get_db()

    connection.execute(
        """
        UPDATE users

        SET
            skills = ?,
            resume_text = ?,
            resume_filename = ?

        WHERE id = ?
        """,
        (
            ",".join(
                detected_skills
            ),
            resume_text,
            filename,
            user_id
        )
    )

    connection.commit()

    connection.close()

    # -----------------------------------------------------
    # STORE AGENT RESULTS IN SESSION
    # -----------------------------------------------------

    session["agent_recommendations"] = (
        result.recommendations
    )

    session["agent_skill_gaps"] = (
        result.skill_gaps
    )

    session["agent_skills"] = (
        result.skills
    )

    # -----------------------------------------------------
    # MESSAGE
    # -----------------------------------------------------

    if not detected_skills:

        flash(
            "Resume uploaded, but no supported skills "
            "were detected."
        )

    else:

        flash(
            "Resume analyzed successfully. "
            + str(len(detected_skills))
            + " skills detected."
        )

    return redirect(
        url_for("recommendations")
    )


# =========================================================
# RECOMMENDATIONS
# =========================================================

@app.route("/recommendations")
def recommendations():

    user_id = session.get(
        "user_id"
    )

    if not user_id:

        return redirect(
            url_for("login")
        )

    connection = get_db()

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    connection.close()

    if not user:

        session.clear()

        return redirect(
            url_for("register")
        )

    # -----------------------------------------------------
    # REQUIRE RESUME
    # -----------------------------------------------------

    resume_text = user["resume_text"] or ""

    if not resume_text.strip():

        flash(
            "Please upload your resume first to get "
            "personalized internship recommendations."
        )

        return redirect(
            url_for("resume")
        )

    # -----------------------------------------------------
    # GET INTERNSHIPS
    # -----------------------------------------------------

    connection = get_db()

    internships = connection.execute(
        """
        SELECT *
        FROM internships
        """
    ).fetchall()

    connection.close()

    internship_list = [
        dict(item)
        for item in internships
    ]

    # -----------------------------------------------------
    # CREATE AGENT STATE
    # -----------------------------------------------------

    state = AgentState(

        user_id=user_id,

        name=user["name"] or "",

        college=user["college"] or "",

        department=user["department"] or "",

        cgpa=user["cgpa"] or "",

        resume_text=resume_text,

        skills=[]
    )

    state.internships = internship_list

    # -----------------------------------------------------
    # RUN CAREER AGENT
    # -----------------------------------------------------

    result = career_agent.run(
        state
    )

    # -----------------------------------------------------
    # GET RESULTS
    # -----------------------------------------------------

    recommendation_list = (
        result.recommendations
    )

    skill_gaps = (
        result.skill_gaps
    )

    detected_skills = (
        result.skills
    )

    # -----------------------------------------------------
    # UPDATE DETECTED SKILLS
    # -----------------------------------------------------

    connection = get_db()

    connection.execute(
        """
        UPDATE users
        SET skills = ?
        WHERE id = ?
        """,
        (
            ",".join(
                detected_skills
            ),
            user_id
        )
    )

    connection.commit()

    connection.close()

    # -----------------------------------------------------
    # STORE RESULTS
    # -----------------------------------------------------

    session["agent_recommendations"] = (
        recommendation_list
    )

    session["agent_skill_gaps"] = (
        skill_gaps
    )

    session["agent_skills"] = (
        detected_skills
    )

    # -----------------------------------------------------
    # RENDER PAGE
    # -----------------------------------------------------

    return render_template(
        "recommendations.html",

        user=user,

        user_skills=detected_skills,

        recommendations=recommendation_list,

        skill_gaps=skill_gaps
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route(
    "/admin",
    methods=["GET", "POST"]
)
def admin():

    user_id = session.get(
        "user_id"
    )

    if not user_id:

        return redirect(
            url_for("login")
        )

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        company = request.form.get(
            "company",
            ""
        ).strip()

        location = request.form.get(
            "location",
            ""
        ).strip()

        skills = request.form.get(
            "skills",
            ""
        ).strip()

        duration = request.form.get(
            "duration",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        if not title or not company:

            flash(
                "Internship title and company are required."
            )

            return redirect(
                url_for("admin")
            )

        connection = get_db()

        connection.execute(
            """
            INSERT INTO internships
            (
                title,
                company,
                location,
                skills,
                duration,
                description
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                title,
                company,
                location,
                skills,
                duration,
                description
            )
        )

        connection.commit()

        connection.close()

        flash(
            "Internship added successfully."
        )

        return redirect(
            url_for("admin")
        )

    connection = get_db()

    internships = connection.execute(
        """
        SELECT *
        FROM internships
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return render_template(
        "admin.html",
        internships=internships
    )


# =========================================================
# EDIT INTERNSHIP
# =========================================================

@app.route(
    "/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit(id):

    user_id = session.get(
        "user_id"
    )

    if not user_id:

        return redirect(
            url_for("login")
        )

    connection = get_db()

    internship = connection.execute(
        """
        SELECT *
        FROM internships
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if not internship:

        connection.close()

        flash(
            "Internship not found."
        )

        return redirect(
            url_for("admin")
        )

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        company = request.form.get(
            "company",
            ""
        ).strip()

        location = request.form.get(
            "location",
            ""
        ).strip()

        skills = request.form.get(
            "skills",
            ""
        ).strip()

        duration = request.form.get(
            "duration",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        connection.execute(
            """
            UPDATE internships

            SET
                title = ?,
                company = ?,
                location = ?,
                skills = ?,
                duration = ?,
                description = ?

            WHERE id = ?
            """,
            (
                title,
                company,
                location,
                skills,
                duration,
                description,
                id
            )
        )

        connection.commit()

        connection.close()

        flash(
            "Internship updated successfully."
        )

        return redirect(
            url_for("admin")
        )

    connection.close()

    return render_template(
        "edit.html",
        internship=internship
    )


# =========================================================
# STUDENTS
# =========================================================

@app.route("/students")
def students():

    user_id = session.get(
        "user_id"
    )

    if not user_id:

        return redirect(
            url_for("login")
        )

    connection = get_db()

    students_list = connection.execute(
        """
        SELECT *
        FROM users
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return render_template(
        "students.html",
        students=students_list
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("index")
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/api/health")
def health():

    return {
        "status": "ok",
        "mode": "local-first",
        "ai_engine": "skill matching and internship recommendation",
        "agent": "CareerAgent",
        "privacy": "resume processing is performed locally"
    }


# =========================================================
# AGENT STATUS
# =========================================================

@app.route("/api/agent-status")
def agent_status():

    return {
        "agent": "CareerAgent",
        "status": "active",
        "tools": [
            "ResumeTool",
            "InternshipTool",
            "RecommendationTool",
            "SkillGapTool"
        ]
    }


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    init_db()

    print()
    print("=" * 60)
    print("AI CAREER AGENT - INTERNSHIP ASSISTANT")
    print("=" * 60)
    print("Server starting...")
    print("Open: http://127.0.0.1:5000")
    print("=" * 60)
    print()

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )