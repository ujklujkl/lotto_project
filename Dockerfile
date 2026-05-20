FROM python:3.12-slim

WORKDIR /app

RUN pip install django==6.0.4 psycopg2-binary

COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]