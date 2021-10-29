FROM python:3.8-slim as backend
WORKDIR /code/src

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src /code/src
ENV PYTHONPATH="/code"
