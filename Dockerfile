# Use python:3.9-slim-buster as the base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
# Combine update, install, and cleanup to reduce layer size
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements.txt file to leverage Docker cache
COPY ./requirements.txt /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose port 5000 for the application
EXPOSE 5000

# Set environment variable for Flask application
ENV FLASK_APP=main.py

# Command to run the Flask application with Gunicorn
CMD ["gunicorn", "--timeout", "300", "-b", ":5000", "main:app"]
