FROM python:3.13-slim

WORKDIR /app

# 1) СНАЧАЛА ставим корневые сертификаты (чтобы HTTPS работал)
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 2) ПОТОМ ставим зависимости Python
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 3) Потом копируем проект
COPY . .

ENV PYTHONUNBUFFERED=1
ENV PORT=8888
ENV DEBUG=0

EXPOSE 8888
CMD ["python", "main.py"]

