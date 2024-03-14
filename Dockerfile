FROM python:3.9-slim

WORKDIR /action

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

ENTRYPOINT ["python", "/action/main.py"]
