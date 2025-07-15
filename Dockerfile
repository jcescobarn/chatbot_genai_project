FROM node:18 AS builder

WORKDIR /frontend
COPY frontend/ ./

RUN npm install && npm run build

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY app/requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY app /app

COPY --from=builder /frontend/out /app/static

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
