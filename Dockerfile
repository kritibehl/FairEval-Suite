FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY evals ./evals
COPY api ./api
COPY benchmark_public ./benchmark_public
COPY exports ./exports
COPY reports ./reports

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e . fastapi uvicorn

EXPOSE 8010

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8010"]
