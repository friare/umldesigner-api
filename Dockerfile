FROM python:3.9

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
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py ./
COPY database.db ./
COPY ./app /app/app

# Expose the application port
EXPOSE 8000
