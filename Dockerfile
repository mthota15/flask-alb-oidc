FROM python:3.7-alpine3.8

WORKDIR /usr/src/app
EXPOSE 8080

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

STOPSIGNAL SIGTERM

CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:8080", "app:app"]
