# interview.py

import random

from utils import ask_gemini, text_to_list
from prompts import (
    HR_QUESTION_PROMPT,
    TECHNICAL_QUESTION_PROMPT
)


class InterviewGenerator:

    def __init__(self):

        self.hr_questions = []
        self.technical_questions = []
        self.all_questions = []


    # ---------------------------------------
    # Generate HR Questions
    # ---------------------------------------
    def generate_hr_questions(self, resume):

        prompt = HR_QUESTION_PROMPT.format(
            resume=resume
        )

        response = ask_gemini(
    prompt +
    "\n\nReturn ONLY the questions. Do NOT write headings, introductions, explanations, or numbering."
)

        print(response)

        self.hr_questions = text_to_list(response)

        return self.hr_questions


    # ---------------------------------------
    # Generate Technical Questions
    # ---------------------------------------
    def generate_technical_questions(self, resume):

        prompt = TECHNICAL_QUESTION_PROMPT.format(
            resume=resume
        )

        response = ask_gemini(
    prompt +
    "\n\nReturn ONLY the questions. Do NOT write headings, introductions, explanations, or numbering."
)

        self.technical_questions = text_to_list(response)

        return self.technical_questions


    # ---------------------------------------
    # Generate Complete Interview
    # ---------------------------------------
    def generate_complete_interview(self, resume):

        self.generate_hr_questions(resume)

        self.generate_technical_questions(resume)

        self.all_questions = (
            self.hr_questions +
            self.technical_questions
        )

        return self.all_questions


    # ---------------------------------------
    # Shuffle Questions
    # ---------------------------------------
    def shuffle_questions(self):

        random.shuffle(self.all_questions)

        return self.all_questions


    # ---------------------------------------
    # Get HR Questions
    # ---------------------------------------
    def get_hr_questions(self):

        return self.hr_questions


    # ---------------------------------------
    # Get Technical Questions
    # ---------------------------------------
    def get_technical_questions(self):

        return self.technical_questions


    # ---------------------------------------
    # Get All Questions
    # ---------------------------------------
    def get_all_questions(self):

        return self.all_questions


    # ---------------------------------------
    # Total Questions
    # ---------------------------------------
    def total_questions(self):

        return len(self.all_questions)


    # ---------------------------------------
    # Question by Index
    # ---------------------------------------
    def get_question(self, index):

        if index >= len(self.all_questions):
            return None

        return self.all_questions[index]


    # ---------------------------------------
    # Print Questions (Debug)
    # ---------------------------------------
    def print_questions(self):

        print("\nHR QUESTIONS\n")

        for i, q in enumerate(self.hr_questions, 1):

            print(f"{i}. {q}")

        print("\nTECHNICAL QUESTIONS\n")

        for i, q in enumerate(self.technical_questions, 1):

            print(f"{i}. {q}")


    # ---------------------------------------
    # Export Questions
    # ---------------------------------------
    def export_questions(self):

        return {

            "hr_questions": self.hr_questions,

            "technical_questions": self.technical_questions,

            "all_questions": self.all_questions

        }