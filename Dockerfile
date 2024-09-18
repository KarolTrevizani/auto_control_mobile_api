FROM python:3.12-slim

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --upgrade pip \
  && pip install -r requirements.txt

COPY . /code/

CMD python manage.py migrate --settings=auto_control.settings.development && python manage.py runserver 0.0.0.0:8000 --settings=auto_control.settings.development