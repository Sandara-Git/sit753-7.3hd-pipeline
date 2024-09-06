


# Your Solution


# Dockerfile for inventory_management microservice

FROM --platform=linux/amd64 python:3.11-slim

# Set the working directory
WORKDIR /usr/src/app

# Copy the inventory_management directory contents into the container
COPY . /usr/src/app

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8001

ENV DATABASE_URL=postgresql://admin:E5OJuKRE14iotwfsvHwJeqsjaKK1eKmO@dpg-cq0nb2aju9rs73b0500g-a.oregon-postgres.render.com/part2

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

