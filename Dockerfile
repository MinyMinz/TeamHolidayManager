FROM python:3.11.4-slim-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /src
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install passlib
RUN pip install -r requirements.txt
COPY ./src /src
EXPOSE 8000