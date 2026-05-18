from utils.ai_helper import ask_ai


class TeachingAssistantAgent:

    def generate(self, topic):

        prompt = f"""
You are Teaching Assistant Agent.

Create a practice workbook for {topic}.

Requirements:
- Beginner exercises
- Intermediate exercises
- Advanced exercises
- Coding challenges
- MCQs
- Assignments
- Mini projects
- Include answers and explanations

Use markdown headings.
"""

        return ask_ai(
            prompt,
            f"Create a practice workbook for {topic}"
        )