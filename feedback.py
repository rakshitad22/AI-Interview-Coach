# feedback.py

from utils import ask_gemini


class FeedbackGenerator:

    def __init__(self):

        self.feedback = ""

    # ----------------------------------------------------
    # Generate Final Feedback
    # ----------------------------------------------------
    def generate_feedback(self, report):

        prompt = f"""
You are an expert interview coach.

Below is the complete interview report.

{report}

Generate a detailed professional feedback.

Return in this format.

Overall Performance

Technical Skills

Communication Skills

Confidence Level

Strengths

Weaknesses

Areas to Improve

Recommended Learning Path

Motivational Message

Final Hiring Recommendation
"""

        self.feedback = ask_gemini(prompt)

        return self.feedback

    # ----------------------------------------------------
    # Overall Performance
    # ----------------------------------------------------
    def overall_performance(self):

        return self.extract_section(
            "Overall Performance"
        )

    # ----------------------------------------------------
    # Technical Skills
    # ----------------------------------------------------
    def technical_skills(self):

        return self.extract_section(
            "Technical Skills"
        )

    # ----------------------------------------------------
    # Communication
    # ----------------------------------------------------
    def communication(self):

        return self.extract_section(
            "Communication Skills"
        )

    # ----------------------------------------------------
    # Confidence
    # ----------------------------------------------------
    def confidence(self):

        return self.extract_section(
            "Confidence Level"
        )

    # ----------------------------------------------------
    # Strengths
    # ----------------------------------------------------
    def strengths(self):

        return self.extract_section(
            "Strengths"
        )

    # ----------------------------------------------------
    # Weaknesses
    # ----------------------------------------------------
    def weaknesses(self):

        return self.extract_section(
            "Weaknesses"
        )

    # ----------------------------------------------------
    # Improvement
    # ----------------------------------------------------
    def improvement(self):

        return self.extract_section(
            "Areas to Improve"
        )

    # ----------------------------------------------------
    # Learning Path
    # ----------------------------------------------------
    def learning_path(self):

        return self.extract_section(
            "Recommended Learning Path"
        )

    # ----------------------------------------------------
    # Motivation
    # ----------------------------------------------------
    def motivation(self):

        return self.extract_section(
            "Motivational Message"
        )

    # ----------------------------------------------------
    # Hiring Recommendation
    # ----------------------------------------------------
    def recommendation(self):

        return self.extract_section(
            "Final Hiring Recommendation"
        )

    # ----------------------------------------------------
    # Extract Section
    # ----------------------------------------------------
    def extract_section(self, heading):

        if self.feedback == "":

            return ""

        lines = self.feedback.split("\n")

        capture = False

        output = []

        for line in lines:

            if heading.lower() in line.lower():

                capture = True

                continue

            if capture:

                if line.strip() == "":

                    break

                if ":" in line and "-" not in line:

                    break

                output.append(line.strip())

        return "\n".join(output)

    # ----------------------------------------------------
    # Export Feedback
    # ----------------------------------------------------
    def export_feedback(self):

        return {

            "Overall Performance":
            self.overall_performance(),

            "Technical Skills":
            self.technical_skills(),

            "Communication":
            self.communication(),

            "Confidence":
            self.confidence(),

            "Strengths":
            self.strengths(),

            "Weaknesses":
            self.weaknesses(),

            "Improvement":
            self.improvement(),

            "Learning Path":
            self.learning_path(),

            "Motivation":
            self.motivation(),

            "Recommendation":
            self.recommendation(),

            "Raw Feedback":
            self.feedback

        }

    # ----------------------------------------------------
    # Reset
    # ----------------------------------------------------
    def reset(self):

        self.feedback = ""