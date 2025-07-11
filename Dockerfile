FROM python:3.13-alpine

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

COPY . /api

WORKDIR /api

EXPOSE 5000

CMD ["gunicorn","-b", "0.0.0.0:5000","app.wsgi:app"]