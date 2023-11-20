FROM python:3.11


RUN mkdir /linguibase

WORKDIR /linguibase

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:666"]