# memory.py

import os
import json
from datetime import datetime


class InterviewMemory:

    def __init__(self):

        self.file = "data/history.json"

        if not os.path.exists("data"):
            os.makedirs("data")

        if not os.path.exists(self.file):

            with open(self.file, "w", encoding="utf-8") as f:

                json.dump({}, f, indent=4)

    # -------------------------------------------------------
    # Load Database
    # -------------------------------------------------------

    def load_database(self):

        with open(self.file, "r", encoding="utf-8") as f:

            return json.load(f)

    # -------------------------------------------------------
    # Save Database
    # -------------------------------------------------------

    def save_database(self, data):

        with open(self.file, "w", encoding="utf-8") as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

    # -------------------------------------------------------
    # Save Interview
    # -------------------------------------------------------

    def save_interview(

        self,

        candidate_name,

        resume_score,

        interview_score,

        questions,

        answers,

        feedback

    ):

        database = self.load_database()

        database[candidate_name] = {

            "date": datetime.now().strftime("%d-%m-%Y %H:%M"),

            "resume_score": resume_score,

            "interview_score": interview_score,

            "questions": questions,

            "answers": answers,

            "feedback": feedback

        }

        self.save_database(database)

    # -------------------------------------------------------
    # Get Candidate
    # -------------------------------------------------------

    def get_candidate(self, candidate):

        database = self.load_database()

        return database.get(candidate)

    # -------------------------------------------------------
    # Candidate Exists
    # -------------------------------------------------------

    def exists(self, candidate):

        database = self.load_database()

        return candidate in database

    # -------------------------------------------------------
    # Delete Candidate
    # -------------------------------------------------------

    def delete_candidate(self, candidate):

        database = self.load_database()

        if candidate in database:

            del database[candidate]

            self.save_database(database)

            return True

        return False

    # -------------------------------------------------------
    # All Candidates
    # -------------------------------------------------------

    def all_candidates(self):

        database = self.load_database()

        return list(database.keys())

    # -------------------------------------------------------
    # Total Interviews
    # -------------------------------------------------------

    def total_interviews(self):

        database = self.load_database()

        return len(database)

    # -------------------------------------------------------
    # Average Interview Score
    # -------------------------------------------------------

    def average_score(self):

        database = self.load_database()

        if len(database) == 0:

            return 0

        scores = []

        for candidate in database.values():

            scores.append(

                candidate["interview_score"]

            )

        return round(

            sum(scores) / len(scores),

            2

        )

    # -------------------------------------------------------
    # Recent Interviews
    # -------------------------------------------------------

    def recent_interviews(self):

        database = self.load_database()

        interviews = []

        for name, details in database.items():

            interviews.append(

                {

                    "Candidate": name,

                    "Date": details["date"],

                    "Score": details["interview_score"]

                }

            )

        interviews.sort(

            key=lambda x: x["Date"],

            reverse=True

        )

        return interviews

    # -------------------------------------------------------
    # Clear Database
    # -------------------------------------------------------

    def clear_database(self):

        self.save_database({})