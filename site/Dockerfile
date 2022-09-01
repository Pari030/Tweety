FROM python:3.10-alpine

WORKDIR /app

ENV TZ="UTC"

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


CMD [ "python3", "-u", "main.py" ]
