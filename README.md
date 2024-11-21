# GitHub Top 100 Parser

## Описание проекта

Этот проект предназначен для парсинга и анализа 100 самых популярных репозиториев GitHub. Данные собираются, обрабатываются и сохраняются в базе данных PostgreSQL, развернутой в кластере Yandex Cloud Managed PostgreSQL.

---

## Содержание

1. [Требования](#требования)
2. [Развертывание локально](#развертывание-локально)
3. [Развертывание в Yandex Cloud](#развертывание-в-yandex-cloud)
4. [Переменные окружения](#переменные-окружения)

---

## Требования

Для работы проекта вам потребуется:
- **Python** >= 3.10
- **PostgreSQL** (рекомендуется Managed PostgreSQL в Yandex Cloud)
- **Docker** и **Docker Compose** (для локального тестирования)
- **Yandex Cloud CLI** для настройки и управления облачной инфраструктурой
- Зависимости Python, указанные в `requirements.txt`


### Развертывание локально

    1. Убедитесь, что у вас установлен Python >= 3.10 и PostgreSQL.  
    2. Установите зависимости:
    pip install -r requirements.txt
    3. Создайте файл .env в корне проекта.
    4. Соберите и запустите приложение в контейнере: docker-compose up --build
    5. Приложение будет доступно по адресу: http://0.0.0.0:8000

    Доступные эндпоинты:

        /api/repos/top100 — список топ-100 репозиториев.
        /api/repos/{owner}/{repo}/activity — информация об активности конкретного репозитория.


## Развертывание в Yandex Cloud
    1. Убедитесь, что у вас настроен Yandex Cloud CLI:
        yc init
    2. Создайте zip-архив с исходным кодом
        zip -r function.zip code requirements.txt
    3. Создайте сервисный аккаунт.
    4. Запустите скрипт deploy_yacloud.sh и следуйте инструкции скрипта.
    5. Настройте переменные окружения через интерфейс Yandex Cloud:
        Зайдите в раздел Cloud Functions.
        Укажите переменные окружения.
    6. Настройте "Подключения к БД" и создайте БД с таблицами. 

## Переменные окружения
    В качестве примера .env:
    DB_NAME=ghpsql
    DB_HOST=rc1b-5p9g4g147bxm77o2.mdb.yandexcloud.net
    DB_PASS=qwertyui
    DB_PORT=6432
    DB_USER=user
    DB_CERT_PATH=/app/root.crt
    DB_SSLMODE=verify-full
    DB_TSA=read-write
