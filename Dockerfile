ARG PYTHON_VERSION=3.12.0a7-slim-bullseye

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y libpq-dev build-essential

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    python -m pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    pip install gunicorn && \
    rm -rf /root/.cache/

RUN mkdir /code/static && \
    mkdir /code/staticfiles && \
    chown -R www-data:www-data /code/static /code/staticfiles && \
    chmod -R 755 /code/static /code/staticfiles

COPY . /code

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "topten.wsgi"]
