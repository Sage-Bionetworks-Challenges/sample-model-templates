FROM python:3.10-slim

WORKDIR /usr/local/bin

COPY requirements.txt .
COPY run_model.py .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "run_model.py"]
