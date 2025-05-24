FROM python:3.12-alpine AS builder

RUN apk add --no-cache gcc musl-dev libffi-dev

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


    FROM python:3.12-alpine

RUN apk add --no-cache curl

RUN addgroup -g 1001 -S appuser && \
    adduser -S appuser -G appuser -u 1001

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /code

COPY --chown=appuser:appuser ./app /code/app

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80/health || exit 1

EXPOSE 80

CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "80"]
