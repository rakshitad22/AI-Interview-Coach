# resume.py

from utils import ask_gemini, read_pdf
from prompts import RESUME_ANALYSIS_PROMPT


class ResumeAnalyzer:
    """
    Handles complete resume analysis.
    """

    def __init__(self):
        self.resume_text = ""
        self.analysis = ""

    def load_resume(self, uploaded_file):
        """
        Reads uploaded PDF resume and extracts text.
        """

        try:
            self.resume_text = read_pdf(uploaded_file)

            if self.resume_text.strip() == "":
                return False, "Resume is empty."

            return True, "Resume Loaded Successfully."

        except Exception as e:
            return False, str(e)

    def analyze_resume(self):
        """
        Sends resume to Gemini for analysis.
        """

        if self.resume_text == "":
            return "Please upload a resume first."

        prompt = RESUME_ANALYSIS_PROMPT.format(
            resume=self.resume_text
        )

        response = ask_gemini(prompt)

        self.analysis = response

        return response

    def get_resume_text(self):
        return self.resume_text

    def get_analysis(self):
        return self.analysis

    def extract_candidate_name(self):
        """
        Attempts to extract candidate name
        from Gemini response.
        """

        if self.analysis == "":
            return "Unknown"

        lines = self.analysis.split("\n")

        for line in lines:

            if "Candidate Name" in line:
                return line.split(":", 1)[-1].strip()

        return "Unknown"

    def extract_resume_score(self):
        """
        Attempts to extract Resume Score.
        """

        if self.analysis == "":
            return 0

        lines = self.analysis.split("\n")

        for line in lines:

            if "Resume Score" in line:

                score = line.split(":")[-1]

                score = score.replace("/100", "")
                score = score.replace("out of 100", "")
                score = score.strip()

                try:
                    return int("".join(filter(str.isdigit, score)))
                except:
                    return 0

        return 0

    def extract_skills(self):
        """
        Extracts skills section.
        """

        if self.analysis == "":
            return []

        lines = self.analysis.split("\n")

        skills = []

        capture = False

        for line in lines:

            if "Skills" in line:
                capture = True
                continue

            if capture:

                if line.strip() == "":
                    break

                skills.append(line.strip("- ").strip())

        return skills

    def summary(self):
        """
        Returns all extracted information.
        """

        return {
            "candidate": self.extract_candidate_name(),
            "resume_score": self.extract_resume_score(),
            "skills": self.extract_skills(),
            "analysis": self.analysis,
            "resume_text": self.resume_text
        }