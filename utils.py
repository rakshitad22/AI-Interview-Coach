# utils.py

import os
import json
import fitz
from dotenv import load_dotenv
from google import genai

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise Exception("GEMINI_API_KEY not found inside .env file.")

# -----------------------------
# Gemini Client
# -----------------------------
client = genai.Client(api_key=API_KEY)

# -----------------------------
# Model Name
# -----------------------------
MODEL_NAME = "gemini-3.6-flash"


# ----------------------------------------------------
# Generic Gemini Function
# ----------------------------------------------------
def ask_gemini(prompt: str) -> str:

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text

    except Exception as e:

        error = str(e)

        if "429" in error:
            return """
⚠️ AI service is temporarily unavailable because the daily request limit has been reached.

Please try again later or use another API key.
"""

        elif "503" in error:
            return """
⚠️ AI service is currently busy.

Please wait a few seconds and try again.
"""

        elif "404" in error:
            return """
⚠️ Selected AI model is unavailable.

Please contact the administrator.
"""

        else:
            return """
⚠️ Unable to connect to Gemini AI.

Please try again later.
"""


# ----------------------------------------------------
# Read PDF Resume
# ----------------------------------------------------
def read_pdf(file):

    document = fitz.open(stream=file.read(), filetype="pdf")

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


# ----------------------------------------------------
# Save JSON
# ----------------------------------------------------
def save_json(data, filename):

    with open(filename, "w", encoding="utf-8") as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


# ----------------------------------------------------
# Load JSON
# ----------------------------------------------------
def load_json(filename):

    if not os.path.exists(filename):
        return {}

    with open(filename, "r", encoding="utf-8") as f:

        return json.load(f)


# ----------------------------------------------------
# Calculate Average Score
# ----------------------------------------------------
def average(scores):

    if len(scores) == 0:
        return 0

    return round(sum(scores) / len(scores), 2)


# ----------------------------------------------------
# Convert Text to List
# ----------------------------------------------------
def text_to_list(text):

    lines = text.split("\n")

    output = []

    for line in lines:

        line = line.strip()

        if line == "":
            continue

        # Skip introductory lines
        if line.lower().startswith("here are"):
            continue

        if "interview questions" in line.lower():
            continue

        # Remove bullets
        if line.startswith("-"):
            line = line[1:].strip()

        # Remove numbering like 1. 2. etc.
        if len(line) > 2 and line[0].isdigit() and "." in line:
            line = line.split(".", 1)[1].strip()

        # Ignore empty lines after cleaning
        if line:
            output.append(line)

    return output   


# ----------------------------------------------------
# Extract Integer Score
# ----------------------------------------------------
def extract_score(text):

    import re

    numbers = re.findall(r"\d+", text)

    if len(numbers) == 0:
        return 0

    score = int(numbers[0])

    if score > 100:
        score = 100

    return score


# ----------------------------------------------------
# Store Interview History
# ----------------------------------------------------
def save_history(candidate, interview_data):

    history = load_json("data/history.json")

    history[candidate] = interview_data

    save_json(history, "data/history.json")


# ----------------------------------------------------
# Read Interview History
# ----------------------------------------------------
def load_history(candidate):

    history = load_json("data/history.json")

    if candidate in history:
        return history[candidate]

    return None