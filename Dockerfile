FROM python:3.12.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ftp_monitor.py .

CMD ["python", "ftp_monitor.py"]