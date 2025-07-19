FROM python:3.9-slim
COPY function.py /app/function.py
CMD ["python3", "/app/function.py"]
