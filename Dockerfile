ARG PYTHON_VERSION=3.12.0
FROM python:${PYTHON_VERSION}-slim as base

LABEL maintainer="silva.vvss12@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /py-planetarium

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN adduser \
    --disabled-password \
    --no-create-home \
    planetarium
RUN chown -R planetarium /py-planetarium
RUN chmod -R 755 /py-planetarium

USER planetarium

