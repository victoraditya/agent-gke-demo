# Use a specific version for reproducibility
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user and switch to it
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Copy application code
COPY . .

# Expose the port
EXPOSE 8080

# Run with Gunicorn
CMD exec uvicorn main:app --host 0.0.0.0 --port $PORT
