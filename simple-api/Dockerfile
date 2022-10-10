FROM python:3.10-slim

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

WORKDIR /app/src

ARG PORT=8080
EXPOSE $PORT

