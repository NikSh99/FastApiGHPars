from github_api import fetch_github_repos, fetch_commit_activity
from data_processing import update_top100_repos  # , fetch_top100_repos
from logging_config import setup_logging
from datetime import datetime
from typing import Dict
import logging

setup_logging()
logger = logging.getLogger(__name__)


def ghtop_parse():
    """Receives data on the top 100 repositories and updates the database."""
    logger.info("Starting the GitHub top repositories parsing process.")

    query = {
        'q': 'stars:>50000',
        'sort': 'stars',
        'order': 'desc',
        'per_page': 100
    }
    try:
        response = fetch_github_repos(query)
        logger.info("Successfully fetched data from GitHub API.")
    except Exception as e:
        logger.error(f"Error fetching data from GitHub API: {e}")
        raise

    if response.get('incomplete_results', True):
        logger.warning("Incomplete data received from GitHub API.")

    repos = response.get('items', [])
    if not repos:
        logger.error("No repository data was received.")
        raise ValueError("No repository data has been received.")

    logger.info(f"Received data for {len(repos)} repositories.")

    data_for_db = [
        (
            repo['full_name'],
            repo['owner']['login'],
            idx + 1,
            None,  # Previous position (if unavailable, None)
            repo['stargazers_count'],
            repo['watchers_count'],
            repo['forks_count'],
            repo['open_issues_count'],
            repo['language']
        )
        for idx, repo in enumerate(repos)
    ]

    update_top100_repos(data_for_db)
    logger.info("Database successfully updated with top 100 repositories.")


def parse_commit_activity(owner: str, repo: str, since: datetime,
                          until: datetime,
                          max_results: int = 1000) -> Dict[str, dict]:
    """Analyzes the activity of the repository (comments and authors)."""
    logger.info(f"Starting commit activity parsing for {owner}/{repo}.")

    params = {
        'since': since.isoformat(),
        'until': until.isoformat(),
        'per_page': 100
    }

    activity_data = {}
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    total_commits = 0

    while url and total_commits < max_results:
        try:
            commits = fetch_commit_activity(owner, repo, params)
            logger.info(f"Fetched {len(commits)} commits from current page.")
        except Exception as e:
            logger.error(f"Error fetching commit data from GitHub API: {e}")
            break

        for commit in commits:
            date = commit['commit']['committer']['date'].split('T')[0]
            author = commit['commit']['author']['name']
            if date not in activity_data:
                activity_data[date] = {'commits': 0, 'authors': set()}
            activity_data[date]['commits'] += 1
            activity_data[date]['authors'].add(author)
            total_commits += 1

        if total_commits >= max_results:
            logger.warning(f"Commit limit reached: {max_results}. Stopping.")
            break

        links = commits.headers.get('Link')
        if links:
            next_link = None
            for link in links.split(','):
                if 'rel="next"' in link:
                    next_link = link.split(";")[0].strip('<>')
                    break
            url = next_link
        else:
            url = None

    for date, data in activity_data.items():
        data['authors'] = list(data['authors'])

    logger.info(f"Processed {total_commits} commits for {owner}/{repo}.")
    return activity_data


def handler(event, context):
    """The entry point for calling the parsing and updating functions."""
    logger.info("The beginning of data parsing.")
    try:
        ghtop_parse()
        logger.info("The parsing is completed.")
    except Exception as e:
        logger.error(f"Error during handler execution: {e}")
        raise
