FROM python:3.12.10
WORKDIR /app

COPY .env /app
COPY requirements.txt /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

