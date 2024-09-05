# Dockerfile for book_catalog microservice
FROM --platform=linux/amd64 python:3.11-slim
WORKDIR /usr/src/app
COPY book_catalog /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
ENV DATABASE_URL=postgresql://sit722_part2_p51z_user:6pgNWhRzOWnfqaRg6IyQ7tV9xY82d7Cx@dpg-cr7u00bqf0us73blansg-a.oregon-postgres.render.com/sit722_part2_p51z
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
