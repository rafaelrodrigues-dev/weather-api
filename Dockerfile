FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml .

RUN apk update && \
    apk upgrade && \
    apk add --no-cache su-exec && \
    rm -rf /var/cache/apk/* && \
    pip install --no-cache-dir --upgrade pip && \
    adduser --disabled-password --no-create-home fuser

COPY src ./src
COPY entrypoint.sh .

RUN pip install --no-cache-dir -e . && \
    chmod +x /app/entrypoint.sh

EXPOSE 5000

CMD ["./entrypoint.sh"]
