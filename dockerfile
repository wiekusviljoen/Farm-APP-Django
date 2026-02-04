# Use a slim Python image
FROM python:3.11-slim

# Keep Python output unbuffered
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system deps for building packages (kept minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the Django dev server port
EXPOSE 8000

# Run migrations and start the development server
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]