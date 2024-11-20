from db_utils import execute_query
from typing import List, Tuple


def update_top100_repos(data: List[Tuple]) -> None:
    """Обновляет топ-100 репозиториев в базе."""
    query = """
        INSERT INTO top_100_repos (repo, owner, position_cur, position_prev,
                                   stars, watchers, forks, open_issues,
                                   language)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (repo) DO UPDATE SET
            position_cur = EXCLUDED.position_cur,
            position_prev = EXCLUDED.position_prev,
            stars = EXCLUDED.stars,
            watchers = EXCLUDED.watchers,
            forks = EXCLUDED.forks,
            open_issues = EXCLUDED.open_issues
    """
    execute_query(query, data)


def fetch_top100_repos() -> list:
    """Возвращает список топ-100 репозиториев."""
    query = """
        SELECT repo, owner, position_cur, position_prev, stars, watchers,
         forks, open_issues, language
        FROM top_100_repos
        ORDER BY stars DESC
        LIMIT 100
    """
    return execute_query(query)


def fetch_current_positions() -> dict:
    """Возвращает текущие позиции репозиториев в топ-100."""
    query = """
        CREATE TABLE IF NOT EXISTS top_100_repos (
            repo VARCHAR(255) PRIMARY KEY,
            owner VARCHAR(255) NOT NULL,
            position_cur INTEGER NOT NULL,
            position_prev INTEGER,
            stars INTEGER NOT NULL,
            watchers INTEGER NOT NULL,
            forks INTEGER NOT NULL,
            open_issues INTEGER NOT NULL,
            language VARCHAR(100)
        )
    """
    execute_query(query)

    query = """
        SELECT repo, position_cur
        FROM top_100_repos
    """
    rows = execute_query(query)
    return dict(rows)
