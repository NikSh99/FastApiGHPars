#!/bin/bash

# Проверяем наличие YC CLI
if ! command -v yc &> /dev/null; then
    echo "Yandex Cloud CLI (yc) не установлен. Пожалуйста, установите его и повторите попытку."
    exit 1
fi

# Проверяем авторизацию
if ! yc config get &> /dev/null; then
    echo "Не выполнена авторизация в Yandex Cloud. Выполните 'yc init' и попробуйте снова."
    exit 1
fi

# Задаём переменные окружения
ENV_VARS_FOR_DB=$(cat <<EOF
DB_HOST=value1
DB_PORT=value2
DB_SSLMODE=value3
DB_CERT_PATH=value4
DB_NAME=value5
DB_USER=value6
DB_PASS=value7
DB_TSA=value8
EOF
)

FUNCTION_NAME="GHPars"

# Создание функции, если она не существует
if yc serverless function get --name="$FUNCTION_NAME" &> /dev/null; then
    echo "Функция $FUNCTION_NAME уже существует."
else
    echo "Создаём функцию $FUNCTION_NAME..."
    yc serverless function create --name="$FUNCTION_NAME"
fi

# Запрос пути к ZIP-файлу
echo "Укажите путь к ZIP-файлу, например: ./github_parser.zip:"
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
  --entrypoint github_parser.handler \
  --memory 128m \
  --execution-timeout 10s \
  --source-path "$FUNCTION_ZIP_PATH" \
  --environment "$ENV_VARS_FOR_DB" && echo "Новая версия функции успешно создана." || echo "Ошибка создания версии функции."

# Настройка триггера
echo "Введите FUNCTION_ID созданной функции (можно узнать через 'yc serverless function get --name=$FUNCTION_NAME'):"
read FUNCTION_ID

echo "Введите SERVICE_ACCOUNT_ID для настройки триггера:"
read SERVICE_ACCOUNT_ID

if yc serverless trigger get --name=timer-for-github-parser &> /dev/null; then
    echo "Триггер timer-for-github-parser уже существует."
else
    echo "Создаём триггер timer-for-github-parser..."
    yc serverless trigger create timer \
      --name timer-for-github-parser \
      --cron-expression '0 */8 * * *' \
      --invoke-function-id "$FUNCTION_ID" \
      --invoke-function-service-account-id "$SERVICE_ACCOUNT_ID" && echo "Триггер успешно создан."
fi

echo "Деплой завершён!"
