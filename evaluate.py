# evaluate.py

import re
from utils import ask_gemini


class InterviewEvaluator:

    def __init__(self):

        self.results = []
        self.total_score = 0

    # -------------------------------------------------
    # Evaluate Single Answer
    # -------------------------------------------------
    def evaluate_answer(self, question, answer):

        prompt = f"""
You are an expert technical interviewer.

Evaluate the following answer.

Question:
{question}

Candidate Answer:
{answer}

Give your response in EXACTLY this format.

Technical Knowledge : <score>/100

Communication : <score>/100

Confidence : <score>/100

Completeness : <score>/100

Overall Score : <score>/100

Strengths:
- point
- point

Weaknesses:
- point
- point

Suggestions:
- point
- point
"""

        response = ask_gemini(prompt)

        print("\n===== GEMINI RESPONSE =====")
        print(response)
        print("===========================\n")
        if response.startswith("Error"):
            return {
                "question": question,
                "answer": answer,
                "evaluation": response,
                "technical": 0,
                "communication": 0,
                "confidence": 0,
                "completeness": 0,
                "overall": 0,
                "strengths": ["Evaluation failed"],
                "weaknesses": ["Gemini API Error"],
                "suggestions": ["Try again later"]
            }

        result = {
            "question": question,
            "answer": answer,
            "evaluation": response,
            
            "technical": self.extract_score(
                response,
                "Technical Knowledge"
            ),
            "communication": self.extract_score(
                response,
                "Communication"
            ),
            "confidence": self.extract_score(
                response,
                "Confidence"
            ),
            "completeness": self.extract_score(
                response,
                "Completeness"
            ),
            "overall": self.extract_score(
                response,
                "Overall Score"
            ),
            "strengths": self.extract_section(
                response,
                "Strengths"
            ),
            "weaknesses": self.extract_section(
                response,
                "Weaknesses"
            ),
            "suggestions": self.extract_section(
                response,
                "Suggestions"
            )
        }

    

        self.results.append(result)

        return result

    # -------------------------------------------------
    # Extract Score
    # -------------------------------------------------
    def extract_score(self, text, field):

        pattern = rf"{re.escape(field)}\s*[:\-]\s*(\d+)"

        match = re.search(pattern, text, re.IGNORECASE)

        if match:

            return int(match.group(1))

        return 0

    # -------------------------------------------------
    # Extract Bullet Section
    # -------------------------------------------------
    def extract_section(self, text, heading):

        lines = text.split("\n")

        capture = False

        data = []

        for line in lines:

            if heading.lower() in line.lower():

                capture = True

                continue

            if capture:

                if line.strip() == "":

                    break

                if ":" in line and "-" not in line:

                    break

                data.append(
                    line.replace("-", "").strip()
                )

        return data

    # -------------------------------------------------
    # Average Overall Score
    # -------------------------------------------------
    def calculate_total_score(self):

        if len(self.results) == 0:

            return 0

        scores = []

        for r in self.results:

            scores.append(r["overall"])

        self.total_score = round(

            sum(scores) / len(scores),

            2

        )

        return self.total_score

    # -------------------------------------------------
    # Technical Average
    # -------------------------------------------------
    def technical_average(self):

        if len(self.results) == 0:

            return 0

        values = []

        for r in self.results:

            values.append(r["technical"])

        return round(sum(values) / len(values), 2)

    # -------------------------------------------------
    # Communication Average
    # -------------------------------------------------
    def communication_average(self):

        if len(self.results) == 0:

            return 0

        values = []

        for r in self.results:

            values.append(r["communication"])

        return round(sum(values) / len(values), 2)

    # -------------------------------------------------
    # Confidence Average
    # -------------------------------------------------
    def confidence_average(self):

        if len(self.results) == 0:

            return 0

        values = []

        for r in self.results:

            values.append(r["confidence"])

        return round(sum(values) / len(values), 2)

    # -------------------------------------------------
    # Completeness Average
    # -------------------------------------------------
    def completeness_average(self):

        if len(self.results) == 0:

            return 0

        values = []

        for r in self.results:

            values.append(r["completeness"])

        return round(sum(values) / len(values), 2)

    # -------------------------------------------------
    # Final Report
    # -------------------------------------------------
    def final_report(self):

        report = {

            "Technical Knowledge":
            self.technical_average(),

            "Communication":
            self.communication_average(),

            "Confidence":
            self.confidence_average(),

            "Completeness":
            self.completeness_average(),

            "Overall Score":
            self.calculate_total_score(),

            "Results":
            self.results

        }

        return report

    # -------------------------------------------------
    # Clear Results
    # -------------------------------------------------
    def reset(self):

        self.results = []

        self.total_score = 0