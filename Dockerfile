# 1. Базовый образ: берём лёгкий Linux (Debian) с уже установленным Python 3.13
FROM python:3.13-slim

# 2. Настройки Python для контейнеров:
# PYTHONDONTWRITEBYTECODE=1 -> не засорять контейнер файлами .pyc
# PYTHONUNBUFFERED=1 -> печатать все логи (print, ошибки) в консоль Docker мгновенно, без задержки в буфере
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Рабочая папка внутри контейнера (как cd /app)
WORKDIR /app

# 4. Ставим системные пакеты Linux:
# - git: ОБЯЗАТЕЛЕН, потому что django-service-objects у тебя скачивается с GitHub!
# - gcc, libpq-dev: нужны на случай компиляции расширений и работы с PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

    
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-interaction --no-ansi --no-root

# 7. Теперь копируем весь остальной код проекта внутрь /app
COPY . /app/

# 8. Сообщаем, что контейнер слушает 8000 порт
EXPOSE 8000