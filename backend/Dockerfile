FROM python:3.9-slim

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
  poppler-utils \
  python3-pip \
  build-essential \
  python3-dev \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Önce requirements.txt'yi kopyala
COPY requirements.txt .

# Python paketlerini yükle
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodlarını kopyala
COPY . .

EXPOSE 5000

CMD ["python", "app.py"] 