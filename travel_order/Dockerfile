FROM python:3.10

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY data data/
COPY models models/
COPY src src/
COPY main_api.py ./

