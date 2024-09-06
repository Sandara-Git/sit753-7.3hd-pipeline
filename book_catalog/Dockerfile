# Dockerfile for book_catalog microservice

FROM --platform=linux/amd64 python:3.11-slim

# Set the working directory
WORKDIR /usr/src/app

# Copy the book_catalog directory contents into the container
COPY . /usr/src/app

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

ENV DATABASE_URL=postgresql://book_catalog_n60i_user:8prUeK5Mdv7yg1bCAPb165m36uefjjmq@dpg-crclg63v2p9s73ci46hg-a.oregon-postgres.render.com/book_catalog_n60i

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


