import os
import google.generativeai as genai

from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def ask_ai(system_prompt, user_prompt):

    try:

        logger.info("Sending request to Gemini")

        full_prompt = f"""
{system_prompt}

User Request:
{user_prompt}
"""

        response = model.generate_content(full_prompt)

        logger.info("Gemini response received")

        return response.text

    except Exception as e:

        logger.error(f"Gemini Error: {str(e)}")

        return f"Error: {str(e)}"