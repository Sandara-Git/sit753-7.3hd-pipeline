# Dockerfile for book_catalog microservice

FROM --platform=linux/amd64 python:3.11-slim

# Set the working directory
WORKDIR /usr/src/app

# Copy the book_catalog directory contents into the container
COPY . /usr/src/app/app
COPY . /usr/src/main.py/app
# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

ENV postgresql://sit772_part3_user:8RkWhS2lk6zAjGBYyLwTOp1PBbpGGCge@dpg-crl3aid6l47c73fqrq60-a.oregon-postgres.render.com/sit772_part3

# Run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


