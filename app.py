# ============================================================
# app.py
# Part 1
# ============================================================

import streamlit as st

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🤖",
    layout="wide"
)

import plotly.graph_objects as go

from resume import ResumeAnalyzer
from interview import InterviewGenerator
from evaluate import InterviewEvaluator
from feedback import FeedbackGenerator
from memory import InterviewMemory


def glass_card(title, value):

    st.markdown(f"""
    <div style="
        backdrop-filter: blur(15px);
        background: rgba(255,255,255,.15);
        border:1px solid rgba(255,255,255,.3);
        border-radius:15px;
        padding:20px;
        box-shadow:0 8px 20px rgba(0,0,0,.15);
        margin-bottom:15px;
    ">
        <h4>{title}</h4>
        <h2>{value}</h2>
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
<style>

.stButton>button{

background:linear-gradient(90deg,#4F46E5,#06B6D4);

color:white;

border:none;

border-radius:10px;

padding:10px;

transition:.3s;

font-weight:bold;

}

.stButton>button:hover{

transform:scale(1.05);

box-shadow:0px 8px 20px rgba(0,0,0,.3);

}

</style>
""",unsafe_allow_html=True)

# ============================================================
# Page Configuration
# ============================================================



def load_css():
    with open("styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()





# ============================================================
# Title
# ============================================================

st.markdown("""
<style>

.main-header{
background: linear-gradient(90deg,#4F46E5,#06B6D4);
padding:25px;
border-radius:15px;
text-align:center;
color:white;
box-shadow:0px 8px 20px rgba(0,0,0,.15);
}

</style>

<div class="main-header">

<h1>🤖 AI Interview Coach</h1>

<h4>Your Personal AI Powered Interview Assistant</h4>

</div>

""", unsafe_allow_html=True)


# ============================================================
# Initialize Objects
# ============================================================

resume_analyzer = ResumeAnalyzer()

interview_generator = InterviewGenerator()

evaluator = InterviewEvaluator()

feedback_generator = FeedbackGenerator()

memory = InterviewMemory()


# ============================================================
# Session State Initialization
# ============================================================

if "resume_uploaded" not in st.session_state:

    st.session_state.resume_uploaded = False


if "resume_text" not in st.session_state:

    st.session_state.resume_text = ""


if "resume_analysis" not in st.session_state:

    st.session_state.resume_analysis = ""


if "candidate_name" not in st.session_state:

    st.session_state.candidate_name = ""


if "resume_score" not in st.session_state:

    st.session_state.resume_score = 0


if "questions" not in st.session_state:

    st.session_state.questions = []


if "answers" not in st.session_state:

    st.session_state.answers = []

if "results" not in st.session_state:
    st.session_state.results = []

if "scores" not in st.session_state:
    st.session_state.scores = []

if "interview_completed" not in st.session_state:
    st.session_state.interview_completed = False


if "current_question" not in st.session_state:

    st.session_state.current_question = 0


if "evaluation_complete" not in st.session_state:

    st.session_state.evaluation_complete = False


if "final_feedback" not in st.session_state:

    st.session_state.final_feedback = ""


# ============================================================
# Sidebar
# ============================================================

st.sidebar.markdown("""
<div style="text-align:center; padding:10px 0 20px 0;">

<h2 style="color:#60A5FA; margin-bottom:0;">
🤖 AI Interview Coach
</h2>

<p style="color:#CBD5E1; font-size:14px;">
Practice • Improve • Get Hired
</p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# Features Card
# ============================================================

st.sidebar.markdown("""
<div style="
background:rgba(255,255,255,.08);
padding:18px;
border-radius:15px;
border:1px solid rgba(255,255,255,.15);
margin-bottom:20px;
">

<h4 style="margin-top:0;">🚀 Features</h4>

📄 Resume Analysis<br><br>
💼 AI Mock Interview<br><br>
📊 Performance Dashboard<br><br>
📚 Interview History

</div>
""", unsafe_allow_html=True)


# ============================================================
# Navigation
# ============================================================

st.sidebar.markdown("### 📂 Navigation")

menu = st.sidebar.radio(
    "",
    [
        "📄 Resume Analysis",
        "💼 Interview",
        "📊 Dashboard",
        "📚 Interview History"
    ]
)


# ============================================================
# Session Information
# ============================================================

st.sidebar.markdown("<br>", unsafe_allow_html=True)

st.sidebar.markdown("### 📈 Session")

resume_score = (
    f"{st.session_state.resume_score}/100"
    if st.session_state.resume_score
    else "--"
)

questions_done = (
    f"{st.session_state.current_question}/{len(st.session_state.questions)}"
    if st.session_state.questions
    else "0/0"
)
st.sidebar.markdown(f"""
<div class="glass">

<b>📄 Resume Score</b>

<h2>{resume_score}</h2>

</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"""
<div class="glass">

<b>📝 Questions</b>

<h2>{questions_done}</h2>

</div>
""", unsafe_allow_html=True)



# ============================================================
# AI Status
# ============================================================

st.sidebar.markdown("<br>", unsafe_allow_html=True)

st.sidebar.success("🤖 Gemini AI Connected")


# ============================================================
# Footer
# ============================================================

st.sidebar.markdown("""
<div style="
text-align:center;
padding:15px;
border-top:1px solid rgba(255,255,255,.15);
margin-top:15px;
">

<h4 style="margin-bottom:8px;">🤖 AI Interview Coach</h4>

<p style="margin:5px 0;color:#CBD5E1;">
Made with ❤️ using
</p>

<p style="margin:5px 0;font-weight:bold;">
Python • Streamlit • Gemini AI
</p>

<p style="margin-top:12px;font-size:12px;color:#94A3B8;">
© 2026 All Rights Reserved
</p>

</div>
""", unsafe_allow_html=True)

# ============================================================
# Resume Upload
# ============================================================

uploaded_file = st.file_uploader(

    "Upload Resume (PDF)",

    type=["pdf"]

)
# ============================================================
# PART 2
# Resume Analysis
# ============================================================

if menu == "📄 Resume Analysis":

    st.header("📄 Resume Analysis")

    if uploaded_file is None:

        st.info("Please upload your resume to begin.")

    else:

        with st.spinner("Reading Resume..."):

            success, message = resume_analyzer.load_resume(uploaded_file)

            st.write("Success:", success)
            st.write("Message:", message)

        if success is True:

            st.success(message)

            st.write("Resume loaded successfully.")

            st.session_state.resume_uploaded = True

            st.session_state.resume_text = resume_analyzer.get_resume_text()

            st.write("Analyze button loaded")

            if st.button("Analyze Resume"):

                with st.spinner("Gemini is analyzing your resume..."):

                    analysis = resume_analyzer.analyze_resume()

                    summary = resume_analyzer.summary()

                    st.session_state.resume_analysis = analysis

                    st.session_state.candidate_name = summary["candidate"]

                    st.session_state.resume_score = summary["resume_score"]

                st.success("Resume Analysis Completed!")

        if st.session_state.resume_analysis != "":

            st.divider()

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("Candidate")

                st.write(st.session_state.candidate_name)

            with col2:

                st.subheader("Resume Score")

                st.metric(

                    label="Score",

                    value=f"{st.session_state.resume_score}/100"

                )

            st.divider()

            st.subheader("Complete Resume Analysis")

            st.markdown(

                st.session_state.resume_analysis

            )

            st.divider()

            st.subheader("Extracted Resume Text")

            with st.expander("View Resume"):

                st.text(

                    st.session_state.resume_text

                )

            st.divider()

            if st.button(
                "Generate Interview Questions",
                disabled=len(st.session_state.questions) > 0
            ):

                with st.spinner(

                    "Generating HR and Technical Questions..."

                ):

                    questions = (

                        interview_generator

                        .generate_complete_interview(

                            st.session_state.resume_text

                        )

                    )

                    st.session_state.questions = questions.copy()

                st.success(

                    f"{len(questions)} Questions Generated Successfully."

                )

                st.info(

                    "Go to the Interview tab from the sidebar."

                )

                # ============================================================
# PART 3
# Interview Page
# ============================================================

elif menu == "💼 Interview":

    st.header("💼 AI Mock Interview")

    if len(st.session_state.questions) == 0:

        st.warning(
            "Generate interview questions first from Resume Analysis."
        )

    else:

        total_questions = len(st.session_state.questions)

        current = st.session_state.current_question

        progress = (current) / total_questions

        st.progress(progress)

        st.caption(f"Completed {current}/{total_questions} Questions")

        st.caption(
            f"Completed {current}/{total_questions} Questions"
        )

        st.write(
            f"Question {current + 1} of {total_questions}"
        )

        st.divider()

        question = st.session_state.questions[current]

        st.subheader("Interview Question")

        st.markdown(f"""
        <div style="
        padding:20px;
        border-radius:15px;
        background:linear-gradient(135deg,#1E293B,#334155);
        border-left:6px solid #38BDF8;
        color:white;
        font-size:18px;
        font-weight:600;
        box-shadow:0 8px 20px rgba(0,0,0,.25);
        ">
        💬 {question}
        </div>
        """, unsafe_allow_html=True)

        answer = st.text_area(

            "Enter your Answer",

            height=220,

            key=f"answer_{current}"

        )

        col1, col2 = st.columns(2)

        with col1:

            submit = st.button("Submit Answer")

        with col2:

            skip = st.button("Skip Question")

        # -----------------------------------------
        # Submit Answer
        # -----------------------------------------

        if submit:

            if answer.strip() == "":

                st.error(
                    "Please enter your answer."
                )

            else:

                with st.spinner(

                    "Evaluating Answer..."

                ):

                    result = evaluator.evaluate_answer(

                        question,

                        answer

                    )

                st.session_state.answers.append(answer)

                print(st.session_state.answers)

                st.session_state.results.append(result)

                evaluator.results = st.session_state.results

                st.session_state.scores.append(

                    result["overall"]

                )

                st.success("Answer Evaluated")

                score = result["overall"]

                if score >= 80:
                    st.success(f"⭐ Overall Score : {score}/100")

                elif score >= 60:
                    st.warning(f"⭐ Overall Score : {score}/100")

                else:
                    st.error(f"⭐ Overall Score : {score}/100")

                st.subheader("Strengths")

                if len(result["strengths"]) == 0:

                    st.write("No strengths returned.")

                else:

                    for item in result["strengths"]:

                        st.success(item)

                st.subheader("Weaknesses")

                if len(result["weaknesses"]) == 0:

                    st.write("No weaknesses returned.")

                else:

                    for item in result["weaknesses"]:

                        st.error(item)

                st.subheader("Suggestions")

                if len(result["suggestions"]) == 0:

                    st.write("No suggestions returned.")

                else:

                    for item in result["suggestions"]:

                        st.info(item)

                if current < total_questions - 1:

                    st.session_state.current_question += 1

                    st.rerun()

                else:

                    st.session_state.interview_completed = True

                    st.success(

                        "Interview Completed!"

                    )

        # -----------------------------------------
        # Skip Question
        # -----------------------------------------

        if skip:

            st.session_state.answers.append("Skipped")

            st.session_state.results.append(

                {

                    "question": question,

                    "answer": "Skipped",

                    "overall": 0,

                    "technical": 0,

                    "communication": 0,

                    "confidence": 0,

                    "completeness": 0,

                    "strengths": [],

                    "weaknesses": [],

                    "suggestions": []

                }

            )

            st.session_state.scores.append(0)

            if current < total_questions - 1:

                st.session_state.current_question += 1

                st.rerun()

            else:

                st.session_state.interview_completed = True

                st.success(

                    "Interview Completed!"

                )

                # ============================================================
# PART 4
# Dashboard
# ============================================================

elif menu == "📊 Dashboard":

    st.header("📊 Interview Dashboard")

    if not st.session_state.interview_completed:

        st.warning("Complete the interview first.")

    else:

        evaluator.results = st.session_state.results
        report = evaluator.final_report()

        col1, col2, col3 = st.columns(3)

        with col1:

            glass_card("📄 Resume Score",
           f"{st.session_state.resume_score}/100")

            

        with col2:

            st.metric(

                "Interview Score",

                f"{report['Overall Score']}/100"

            )

        with col3:

            if report["Overall Score"] >= 75:

                status = "Selected ✅"

            elif report["Overall Score"] >= 50:

                status = "Average ⚠️"

            else:

                status = "Rejected ❌"

            st.metric(

                "Result",

                status

            )

        st.divider()

        st.subheader("📊 Performance")

        c1, c2 = st.columns(2)

        with c1:
            st.metric("Technical", report["Technical Knowledge"])
            st.metric("Communication", report["Communication"])

        with c2:
            st.metric("Confidence", report["Confidence"])
            st.metric("Completeness", report["Completeness"])

        st.divider()

        st.subheader("📈 Skill Analysis")

        scores = [
            report["Technical Knowledge"],
            report["Communication"],
            report["Confidence"],
            report["Completeness"]
        ]

        labels = [
            "Technical",
            "Communication",
            "Confidence",
            "Completeness"
        ]

        fig = go.Figure()

        fig.add_trace(
            go.Scatterpolar(
                r=scores,
                theta=labels,
                fill='toself',
                name="Performance"
            )
        )

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Question-wise Scores")

        for i, result in enumerate(report["Results"]):

            with st.expander(

                f"Question {i+1}"

            ):

                st.write(

                    "**Question**"

                )

                st.write(

                    result["question"]

                )

                st.write(

                    "**Answer**"

                )

                st.write(

                    result["answer"]

                )

                st.metric(

                    "Overall Score",

                    result["overall"]

                )

                st.write(

                    "**✅ Strengths**"

                )

                for item in result["strengths"]:

                    st.success(item)

                st.write(

                    "**⚠️ Weaknesses**"

                )

                for item in result["weaknesses"]:

                    st.error(item)

                st.write(

                    "**💡 Suggestions**"

                )

                for item in result["suggestions"]:

                    st.info(item)

        st.divider()

        st.subheader("AI Final Feedback")

        if st.button(

            "Generate Final Feedback"

        ):

            with st.spinner(

                "Generating..."

            ):

                feedback = (

                    feedback_generator

                    .generate_feedback(

                        report

                    )

                )

                st.session_state.final_feedback = feedback

        if st.session_state.final_feedback != "":

            st.markdown(

                st.session_state.final_feedback

            )

        st.divider()

        if st.button(

            "Save Interview"

        ):

            memory.save_interview(

                candidate_name=

                st.session_state.candidate_name,

                resume_score=

                st.session_state.resume_score,

                interview_score=

                report["Overall Score"],

                questions=

                st.session_state.questions,

                answers=

                st.session_state.answers,

                feedback=

                st.session_state.final_feedback

            )

            st.success(

                "Interview Saved Successfully."

            )
            # ============================================================
# PART 5
# Interview History
# ============================================================

elif menu == "📚 Interview History":

    st.header("📚 Interview History")

    candidates = memory.all_candidates()

    if len(candidates) == 0:

        st.info("No interview history available.")

    else:

        st.success(

            f"Total Interviews : {memory.total_interviews()}"

        )

        st.metric(

            "Average Interview Score",

            memory.average_score()

        )

        st.divider()

        selected_candidate = st.selectbox(

            "Select Candidate",

            candidates

        )

        details = memory.get_candidate(

            selected_candidate

        )

        if details is not None:

            st.subheader("Candidate Information")

            col1, col2 = st.columns(2)

            with col1:

                st.write(

                    "**Candidate Name**"

                )

                st.write(selected_candidate)

                st.write(

                    "**Resume Score**"

                )

                st.write(

                    details["resume_score"]

                )

            with col2:

                st.write(

                    "**Interview Score**"

                )

                st.write(

                    details["interview_score"]

                )

                st.write(

                    "**Interview Date**"

                )

                st.write(

                    details["date"]

                )

            st.divider()

            st.subheader("Interview Questions")

            for i, question in enumerate(

                details["questions"]

            ):

                with st.expander(

                    f"Question {i+1}"

                ):

                    st.write(question)

                    if i < len(details["answers"]):

                        st.write(

                            "**Candidate Answer**"

                        )

                        st.write(

                            details["answers"][i]

                        )

            st.divider()

            st.subheader("Final Feedback")

            st.markdown(

                details["feedback"]

            )

            st.divider()

            col1, col2 = st.columns(2)

            with col1:

                if st.button(

                    "Delete This Interview"

                ):

                    memory.delete_candidate(

                        selected_candidate

                    )

                    st.success(

                        "Interview Deleted Successfully."

                    )

                    st.rerun()

            with col2:

                if st.button(

                    "Delete Complete History"

                ):

                    memory.clear_database()

                    st.success(

                        "All Interview History Deleted."

                    )

                    st.rerun()

        st.divider()

        st.subheader("Recent Interviews")

        interviews = memory.recent_interviews()

        for interview in interviews:

            with st.container():

                st.write(

                    f"👤 {interview['Candidate']}"

                )

                st.write(

                    f"📅 {interview['Date']}"

                )

                st.write(

                    f"⭐ Score : {interview['Score']}"

                )

                st.divider()

                # ============================================================
# PART 6
# Reset Interview & Footer
# ============================================================

st.divider()

st.sidebar.header("Settings")

if st.sidebar.button("🔄 Start New Interview"):

    st.session_state.resume_uploaded = False
    st.session_state.resume_text = ""
    st.session_state.resume_analysis = ""
    st.session_state.candidate_name = ""
    st.session_state.resume_score = 0

    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.results = []
    st.session_state.scores = []

    st.session_state.current_question = 0
    st.session_state.interview_completed = False
    st.session_state.evaluation_complete = False
    st.session_state.final_feedback = ""

    resume_analyzer = ResumeAnalyzer()
    interview_generator = InterviewGenerator()
    evaluator = InterviewEvaluator()
    feedback_generator = FeedbackGenerator()

    st.success("Ready for a new interview!")

    st.rerun()


st.sidebar.divider()

st.sidebar.subheader("Application Status")

if st.session_state.resume_uploaded:

    st.sidebar.success("✅ Resume Uploaded")

else:

    st.sidebar.error("❌ Resume Not Uploaded")


if len(st.session_state.questions) > 0:

    st.sidebar.success(
        f"✅ Questions Generated ({len(st.session_state.questions)})"
    )

else:

    st.sidebar.warning("Questions Not Generated")


if st.session_state.interview_completed:

    st.sidebar.success("✅ Interview Completed")

else:

    st.sidebar.info("Interview In Progress")


st.sidebar.divider()

st.markdown("""
<hr style="border:1px solid #2E3B55;">

<div style="
background:linear-gradient(135deg,#0F172A,#1E293B,#0F766E);
padding:30px;
border-radius:20px;
color:white;
box-shadow:0px 8px 25px rgba(0,0,0,.35);
">

<h2 style="text-align:center;">
🚀 AI Interview Coach
</h2>

<p style="text-align:center;font-size:18px;color:#D1D5DB;">
Empowering candidates with AI-driven resume analysis, mock interviews,
real-time evaluation, and personalized feedback.
</p>

<hr style="border:1px solid rgba(255,255,255,.2);">

<div style="display:flex;justify-content:space-around;flex-wrap:wrap;">

<div>
<h4>✨ Features</h4>

✔ Resume Analysis<br>
✔ AI Interview Questions<br>
✔ Smart Answer Evaluation<br>
✔ Performance Dashboard<br>
✔ Interview History

</div>

<div>
<h4>🛠 Tech Stack</h4>

🐍 Python<br>
⚡ Streamlit<br>
🤖 Google Gemini AI<br>
📊 Plotly<br>
💾 SQLite / JSON

</div>

<div>
<h4>👩‍💻 Developer</h4>

Rakshita D<br>
Information Science Engineering<br>
Sri Krishna Institute of Technology<br>
Aspiring Software Developer

</div>

</div>

<br>

<hr style="border:1px solid rgba(255,255,255,.2);">

<p style="text-align:center;color:#CBD5E1;">

© 2026 AI Interview Coach • Built with ❤️ using Python, Streamlit & Google Gemini AI

</p>

</div>

""", unsafe_allow_html=True)