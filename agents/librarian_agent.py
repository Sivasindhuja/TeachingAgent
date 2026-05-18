from utils.ai_helper import ask_ai
from utils.resource_search import search_resources


class LibrarianAgent:

    def generate(self, topic):

        resources = search_resources(topic)

        prompt = f"""
You are Research Librarian Agent.

Below are collected web resources.

{resources}

Your task:
- Organize resources properly
- Categorize by difficulty
- Mention why resource is useful
- Include books, videos, documentation, tutorials
- Create a structured resource guide

Use markdown headings.
"""

        return ask_ai(
            prompt,
            f"Create a resource guide for learning {topic}"
        )