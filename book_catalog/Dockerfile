# Dockerfile for book_catalog microservice

FROM --platform=linux/amd64 python:3.11-slim

# Set the working directory
WORKDIR /usr/src/app

# Copy the book_catalog directory contents into the container
COPY book_catalog/ /usr/src/app
COPY main.py /usr/src/app/

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

