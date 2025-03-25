FROM python:3.9-slim

# Install PostgreSQL dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make the start script executable
RUN chmod +x start.sh

# Expose the application port
EXPOSE ${PORT:-5005}

# Use the start script as the entry point
CMD ["./start.sh"] 