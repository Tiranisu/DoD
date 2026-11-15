FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip insrall -r requirements.txt

COPY . .
CMD ["python", "main.py"]
