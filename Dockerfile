
# Use a lightweight Python 3.8 image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY index/api.py ./index/api.py
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for Flask server
EXPOSE 5000

# Command to run the Flask server
CMD ["python", "./index/api.py"]
