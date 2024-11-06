FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-slim

COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

RUN apt-get update && apt-get install -y postgresql-client

ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword
ENV POSTGRES_DB=mydb

RUN psql -U $POSTGRES_USER -c "CREATE DATABASE $POSTGRES_DB;"

RUN psql -U $POSTGRES_USER -d $POSTGRES_DB -f /app/schema.sql

WORKDIR /app

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

