FROM tiangolo/uvicorn-gunicorn:python3.8

LABEL maintainer="Fox Maltas <fox@foxhawk.co.uk>"

COPY . /app

RUN pip install --no-cache-dir fastapi
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt