import requests
import logging

logger = logging.getLogger(__name__)


def fetch_github_repos(query: dict) -> dict:
    """Requests a list of repositories via the GitHub API."""
    url = "https://api.github.com/search/repositories"
    try:
        logger.info(f"Sending request to GitHub API with query: {query}")
        response = requests.get(url, params=query)
        response.raise_for_status()
        logger.info(f"Received response: {response.status_code}")
        logger.info("The request to GitHub API was completed successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"GitHub API request error: {e}")
        raise


def fetch_commit_activity(owner: str, repo: str, params: dict) -> list:
    """Requests commits for the repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        logger.info(f"Commit data for {repo} has been successfully received.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error requesting repository activity: {e}")
        raise
