from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List, Optional, Literal
from datetime import datetime, timezone, date
import logging

# Импортируем функции из сервисного модуля
from data_processing import fetch_top100_repos
from ghpars import parse_commit_activity
from validation import validate_dates

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GitHub Repositories API",
    description="API для получения информации о репозиториях GitHub",
    version="1.0.0"
)


# Модель для эндпоинта /api/repos/top100
class Repo(BaseModel):
    repo: str
    owner: str
    position_cur: int
    position_prev: Optional[int]
    stars: int
    watchers: int
    forks: int
    open_issues: int
    language: Optional[str]


# Модель для эндпоинта /api/repos/{owner}/{repo}/activity
class ActivityDay(BaseModel):
    date: date
    commits: int
    authors: List[str]


@app.get("/api/repos/top100", response_model=List[Repo],
         summary="Top 100 репозиториев",
         description="Возвращает список топ-100 репозиториев.")
def top_100_repos(
    sort: str = Query('position_cur', description="Поле для сортировки"),
    order: Literal['asc', 'desc'] = Query('asc', description="Порядок сортировки (asc/desc)")
):
    try:
        rows = fetch_top100_repos()
        if not rows:
            raise HTTPException(status_code=404, detail="No repositories found in the database.")

        repos = [
            Repo(
                repo=row[0],
                owner=row[1],
                position_cur=row[2],
                position_prev=row[3],
                stars=row[4],
                watchers=row[5],
                forks=row[6],
                open_issues=row[7],
                language=row[8]
            )
            for row in rows
        ]

        repos.sort(key=lambda item: getattr(item, sort), reverse=(order == 'desc'))
        logger.info(f"Returned {len(repos)} repositories sorted by {sort} in {order} order.")
        return repos

    except Exception as e:
        logger.error(f"Error while fetching top 100 repos: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/repos/{owner}/{repo}/activity", response_model=List[ActivityDay],
         summary="Activity for a repository",
         description="Возвращает активность по дням для указанного репозитория.")
def show_repo_activity(
    owner: str,
    repo: str,
    dates: tuple[datetime, datetime] = Depends(validate_dates)
):
    try:
        since, until = dates
        activity_data = parse_commit_activity(owner, repo, since, until)
        if not activity_data:
            raise HTTPException(status_code=404, detail=f"No activity data found for repository {owner}/{repo}.")

        days = [
            ActivityDay(
                date=key,
                commits=activity_data[key]['commits'],
                authors=activity_data[key]['authors']
            )
            for key in activity_data
        ]

        days.sort(key=lambda item: item.date, reverse=True)
        logger.info(f"Returned activity data for repo '{repo}' by '{owner}' from {since} to {until}.")
        return days

    except HTTPException as e:
        logger.warning(f"User error: {str(e)}")
        raise

    except Exception as e:
        logger.error(f"Error while fetching activity data: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
