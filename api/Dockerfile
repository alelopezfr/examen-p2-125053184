FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Configurar SSH en el cliente API para conectarse a Hadoop sin contraseña
RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh && \
    echo "Host *\n  StrictHostKeyChecking no\n  UserKnownHostsFile=/dev/null\n" >> /root/.ssh/config

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]