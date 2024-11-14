FROM python:3.10

WORKDIR /app

COPY travel_order/requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY travel_order/data data/
COPY ../models/ models/
COPY travel_order/src src/
COPY travel_order/main_api.py ./

