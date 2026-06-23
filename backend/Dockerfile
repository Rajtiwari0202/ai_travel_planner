FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt \
    && addgroup --system app \
    && adduser --system --ingroup app app \
    && mkdir -p /data \
    && chown -R app:app /app /data

COPY --chown=app:app backend /app
USER app

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/v1/health/ready', timeout=3).read()"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
