

FROM --platform=linux/amd64 python:3.11-slim
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app
EXPOSE 8001
ENV DATABASE_URL=postgresql://sit772_part3_user:8RkWhS2lk6zAjGBYyLwTOp1PBbpGGCge@dpg-crl3aid6l47c73fqrq60-a.oregon-postgres.render.com/sit772_part3
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]


