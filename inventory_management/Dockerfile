

# Use an official Python runtime as a parent image
FROM  --platform=linux/amd6 python:3.11-slim

# Set the working directory
WORKDIR /usr/src/app

# Copy the inventory_management directory contents into the container
COPY inventory_management/ /usr/src/app

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8001

# Run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
