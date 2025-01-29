# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose the default Cloud Run port
EXPOSE 8080

# Run the application
CMD ["python", "auth.py"]
# # Run app.py when the container launches
# CMD ["python", "main.py"]