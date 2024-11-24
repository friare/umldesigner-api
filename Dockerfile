FROM python:latest

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-distutils \
    build-essential \
    gcc \
    && apt-get clean

# Copy requirements and install Python dependencies
COPY requirements.txt ./
COPY main.py ./
COPY database.db ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./app /app/app
EXPOSE 8000
