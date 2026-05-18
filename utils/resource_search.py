
import os

from serpapi import GoogleSearch
from dotenv import load_dotenv

from utils.logger import logger

load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


def search_resources(topic):

    try:

        logger.info(f"Searching resources for {topic}")

        params = {
            "engine": "google",
            "q": f"best resources to learn {topic}",
            "api_key": SERPAPI_API_KEY,
            "num": 10
        }

        search = GoogleSearch(params)

        results = search.get_dict()

        resources = []

        if "organic_results" in results:

            for item in results["organic_results"][:10]:

                title = item.get("title", "No Title")

                link = item.get("link", "")

                snippet = item.get("snippet", "")

                resources.append(
                    f"""
Title: {title}

Link: {link}

Description: {snippet}
"""
                )

        logger.info("Resource search completed")

        return "\n\n".join(resources)

    except Exception as e:

        logger.error(f"Search Error: {str(e)}")

        return "Failed to fetch resources"