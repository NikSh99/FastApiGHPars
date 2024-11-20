from fastapi import HTTPException
from datetime import datetime, timezone
from typing import Optional


def validate_dates(
    since: Optional[datetime] = None, 
    until: Optional[datetime] = None
) -> tuple[datetime, datetime]:
    """
    Проверяет и валидирует параметры 'since' и 'until'. Преобразует их в формат с временной зоной UTC.
    Если параметры некорректны, выбрасывает HTTPException с ошибкой.

    :param since: Дата начала в формате ISO 8601.
    :param until: Дата окончания в формате ISO 8601.
    :return: Кортеж с двумя объектами datetime.
    """

    if since is None or until is None:
        raise HTTPException(status_code=400, detail="Please provide both 'since' and 'until' parameters in ISO 8601 format.")

    if since.tzinfo is None:
        since = since.replace(tzinfo=timezone.utc)
    if until.tzinfo is None:
        until = until.replace(tzinfo=timezone.utc)

    if until <= since:
        raise HTTPException(status_code=400, detail="'until' must be greater than 'since'")

    return since, until
