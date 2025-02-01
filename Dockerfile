FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn requests python-dotenv
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
