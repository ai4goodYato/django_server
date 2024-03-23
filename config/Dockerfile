FROM python:3
WORKDIR /usr/src/app

RUN python -m venv venv

RUN /bin/bash -c "source venv/bin/activate"
COPY requirements.txt .
COPY .env .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx

ENV DJANGO_SETTINGS_MODULE=config.settings

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]