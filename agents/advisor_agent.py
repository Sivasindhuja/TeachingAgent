from utils.ai_helper import ask_ai


class AdvisorAgent:

    def generate(self, topic):

        prompt = f"""
You are Academic Advisor Agent.

Create a complete learning roadmap for {topic}.

Requirements:
- Beginner to advanced roadmap
- Weekly milestones
- Time estimates
- Prerequisites
- Project recommendations
- Interview preparation roadmap
- Revision strategy

Use proper markdown headings.
"""

        return ask_ai(
            prompt,
            f"Create a learning roadmap for {topic}"
        )