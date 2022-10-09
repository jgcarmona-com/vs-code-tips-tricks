FROM python:3.10-slim
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Set location of pip.conf
ENV PIP_CONFIG_FILE $PWD/pip.conf

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt


WORKDIR /app
COPY . /app

WORKDIR /app/src

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

ARG PORT=8080
ENV PORT=$PORT
EXPOSE $PORT

