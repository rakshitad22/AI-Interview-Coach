# prompts.py

# ==========================================================
# RESUME ANALYSIS
# ==========================================================

RESUME_ANALYSIS_PROMPT = """
You are an experienced HR recruiter.

Analyze the following resume.

Return the response in the following format only.

Candidate Name:

Education:

Skills:

Projects:

Experience:

Certifications:

Strengths:

Weaknesses:

Missing Skills:

Resume Score (out of 100):

Resume:

{resume}
"""


# ==========================================================
# HR QUESTIONS
# ==========================================================

HR_QUESTION_PROMPT = """
You are an HR interviewer.

Generate exactly 5 HR interview questions based on the candidate's resume.

Rules:

1. Questions must be unique.
2. Questions must be beginner friendly.
3. Don't include answers.
4. Number the questions.

Resume:

{resume}
"""


# ==========================================================
# TECHNICAL QUESTIONS
# ==========================================================

TECHNICAL_QUESTION_PROMPT = """
You are a senior software engineer.

Generate exactly 5 technical interview questions based on the candidate's resume.

Rules:

1. Questions should test skills mentioned in the resume.
2. Beginner to Intermediate level.
3. Don't include answers.
4. Number the questions.

Resume:

{resume}
"""


# ==========================================================
# ANSWER EVALUATION
# ==========================================================

ANSWER_EVALUATION_PROMPT = """
You are an expert technical interviewer.

Evaluate the candidate's answer.

Question:

{question}

Candidate Answer:

{answer}

Evaluate using:

Technical Knowledge

Communication

Accuracy

Confidence

Completeness

Finally return:

Overall Score : xx/100

Strengths

Weaknesses

Suggestions
"""


# ==========================================================
# FINAL FEEDBACK
# ==========================================================

FINAL_FEEDBACK_PROMPT = """
You are an interview coach.

Using all interview evaluations below,

Generate a final interview report.

Interview Details

{evaluation}

Return the report in the following format.

Overall Performance

Technical Skills

Communication Skills

Confidence Level

Strengths

Weaknesses

Areas to Improve

Final Score (out of 100)

Motivational Message
"""