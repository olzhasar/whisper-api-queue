FROM python:3.11

ENV PYTHONBUFFERED=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_VERSION=1.5.1

RUN apt update && apt -y install ffmpeg
RUN pip install --upgrade pip && pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry export --without-hashes -f requirements.txt | pip install -r /dev/stdin

COPY . .

CMD ["celery", "-A", "app:app", "worker"]
