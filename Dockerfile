# Use an official Python runtime as a parent image
FROM python:3.12.11-slim

# Set working directory in the container
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Убедимся, что start.sh исполняемый
RUN chmod +x /app/start.sh

EXPOSE 8000

# Используем скрипт запуска
CMD ["./start.sh"]
