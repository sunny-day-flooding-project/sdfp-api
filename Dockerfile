#FROM python:3.9
FROM pypy:3.9-slim-buster

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

EXPOSE 5432

CMD ["pypy", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
