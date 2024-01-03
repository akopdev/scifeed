FROM python:3.9-slim

WORKDIR /

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN playwright install
RUN playwright install-deps

COPY ./scifeed /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
