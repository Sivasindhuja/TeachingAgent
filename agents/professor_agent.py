from utils.ai_helper import ask_ai


class ProfessorAgent:

    def generate(self, topic):

        prompt = f"""
You are Professor Agent.

Your job:
Create a COMPLETE knowledge base document for learning {topic}.

Requirements:
- Beginner friendly
- Structured properly
- Use headings and subheadings
- Include examples
- Include real world applications
- Include important terminology
- Include summary section
- Include advanced concepts

Format properly using markdown headings.
"""

        return ask_ai(
            prompt,
            f"Create a complete knowledge base for {topic}"
        )