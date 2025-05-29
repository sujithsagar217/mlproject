# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy dependencies file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . .

# Expose Flask port
EXPOSE 5000

# Set environment variable to make Flask run on 0.0.0.0
ENV FLASK_RUN_HOST=0.0.0.0

# Run the app
CMD ["python", "app.py"]
