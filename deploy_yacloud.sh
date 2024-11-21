#!/bin/bash

# Проверяем наличие YC CLI
if ! command -v yc &> /dev/null; then
    echo "Yandex Cloud CLI (yc) не установлен. Пожалуйста, установите его и повторите попытку."
    exit 1
fi

yc init

# Задаём переменные окружения
# ENV_VARS_FOR_DB="DB_NAME=ghpsql,DB_HOST=rc1b-5p9g4g147bxm77o2.mdb.yandexcloud.net,rc1d-emqut7to4cmmpnxn.mdb.yandexcloud.net,DB_PASS=!QAZ2wsx,DB_PORT=6432,DB_USER=user,DB_CERT_PATH=/root.crt,DB_SSLMODE=verify-full,DB_TSA=read-write"

FUNCTION_NAME="gh-pars"

# Создание функции, если она не существует
if yc serverless function get --name="$FUNCTION_NAME" &> /dev/null; then
    echo "Функция $FUNCTION_NAME уже существует."
else
    echo "Создаём функцию $FUNCTION_NAME..."
    yc serverless function create --name="$FUNCTION_NAME"
fi

# Запрос пути к ZIP-файлу
echo "Укажите путь к ZIP-файлу, например: ./ghpars.zip:"
read FUNCTION_ZIP_PATH

if [ ! -f "$FUNCTION_ZIP_PATH" ]; then
    echo "Указанный файл $FUNCTION_ZIP_PATH не существует. Проверьте путь и попробуйте снова."
    exit 1
fi

# Создание новой версии функции
echo "Загружаем новую версию функции..."
yc serverless function version create \
  --function-name "$FUNCTION_NAME" \
  --runtime python311 \
  --entrypoint ghpars.handler \
  --memory 128m \
  --execution-timeout 10s \
  --source-path "$FUNCTION_ZIP_PATH" \
 --environment "DB_NAME=ghpsql DB_HOST=rc1b-5p9g4g147bxm77o2.mdb.yandexcloud.net DB_PASS=1qaz2wsx DB_PORT=6432 DB_USER=user DB_CERT_PATH=/root.crt DB_SSLMODE=verify-full DB_TSA=read-write" && echo "Новая версия функции успешно создана." || echo "Ошибка создания версии функции."

# Настройка триггера
echo "Введите FUNCTION_ID:"
read FUNCTION_ID

echo "Введите SERVICE_ACCOUNT_ID:"
read SERVICE_ACCOUNT_ID

if yc serverless trigger get --name=gh-pars &> /dev/null; then
    echo "Триггер gh-pars уже существует."
else
    echo "Создаём триггер gh-pars..."
    yc serverless trigger create timer \
      --name gh-pars \
      --cron-expression "* * */4 * * *" \
      --invoke-function-id "$FUNCTION_ID" \
      --invoke-function-service-account-id "$SERVICE_ACCOUNT_ID" && echo "Триггер успешно создан."
fi

echo "Деплой завершён!"
