FROM python:3.11.4-slim-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .env .
COPY grade_checker.py .

ENTRYPOINT ["python", "grade_checker.py"]