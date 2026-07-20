FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

COPY . /api

WORKDIR /api

EXPOSE 5000

RUN apk update && \
    apk upgrade && \
    pip install --upgrade pip && \
    pip install -r /api/requirements.txt && \
    apk add --no-cache su-exec && \
    adduser --disabled-password --no-create-home fuser && \
    chmod +x /api/entrypoint.sh


CMD [ "./entrypoint.sh"]