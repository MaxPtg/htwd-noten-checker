FROM python:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .env .
COPY grade_grabber.py .

ENTRYPOINT ["python", "grade_grabber.py"]