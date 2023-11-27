FROM python:3.11-slim

WORKDIR /app

COPY ./ ./

RUN pip3 install -r requirements.txt --no-cache-dir
RUN python manage.py makemigrations cafe tables menu admin_users reservation
RUN python manage.py migrate
RUN python manage.py collectstatic --no-input

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8080", "azu_bot_django.asgi:application"]  