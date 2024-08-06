FROM python:3.10-slim

# Tesseract ve diğer bağımlılıkları yükleyin
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    ocrmypdf \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p /usr/src/app/tmp

CMD ["watchmedo", "auto-restart", "--directory=.", "--pattern=*.py", "--recursive", "python main.py"]
