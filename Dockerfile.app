FROM python:3.12-alpine AS builder

WORKDIR /build

RUN apk add --no-cache gcc musl-dev

COPY ./requirements.txt /build/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-alpine AS production

WORKDIR /code

COPY --from=builder /root/.local /root/.local

COPY ./app /code/app

ENV PATH=/root/.local/bin:$PATH

EXPOSE 80

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
