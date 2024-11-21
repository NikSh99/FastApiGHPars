FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ghpars.py validation.py logging_config.py github_api.py db_utils.py data_processing.py .env root.crt ./

ENV DB_CERT_PATH=/app/root.crt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
