FROM python:3.9

WORKDIR /

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./scifeed /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
