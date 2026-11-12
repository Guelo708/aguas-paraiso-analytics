FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

RUN groupadd --system appgroup \
    && useradd \
        --system \
        --gid appgroup \
        --create-home \
        appuser

COPY requirements.txt ./

RUN python -m pip install \
    --no-cache-dir \
    --upgrade pip \
    && python -m pip install \
        --no-cache-dir \
        -r requirements.txt

COPY app ./app

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

HEALTHCHECK \
    --interval=30s \
    --timeout=5s \
    --start-period=20s \
    --retries=3 \
    CMD python -c \
    "import urllib.request; urllib.request.urlopen('http://127.0.0.1:' + __import__('os').environ.get('PORT', '8000') + '/health')"

CMD [
    "sh",
    "-c",
    "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"
]
