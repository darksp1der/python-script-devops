FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY application/ImportLogs.py /app/
COPY application/Solve.py /app/
COPY tests/Test.py /app/
COPY tests/UnitTest.py /app/
COPY run.sh /app/

RUN chmod +x /app/run.sh

ENTRYPOINT ["/app/run.sh"]