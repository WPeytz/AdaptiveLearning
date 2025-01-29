# Use a lightweight base image
FROM python:3.11-slim

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port 8080
EXPOSE 8080

# Run the app
CMD ["python", "auth.py"]

# # Run app.py when the container launches
# CMD ["python", "main.py"]