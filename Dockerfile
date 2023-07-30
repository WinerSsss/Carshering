FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SECRET_KEY="SECRET_KEY"
ENV DEBUG=True

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/

RUN pip install -r requirements.txt && \
    python manage.py makemigrations carservice && \
    python manage.py makemigrations users && \
    python manage.py migrate carservice && \
    python manage.py migrate users && \
    python manage.py makemigrations && \
    python manage.py migrate


EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
