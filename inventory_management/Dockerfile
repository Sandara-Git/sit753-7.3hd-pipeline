


FROM  --platform=linux/amd6 python:3.11-slim
WORKDIR /usr/src/app
COPY inventory_management/ /usr/src/app
COPY main.py /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
