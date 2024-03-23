FROM python:3
WORKDIR /usr/src/app

RUN python -m venv venv

RUN /bin/bash -c "source venv/bin/activate"
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV DJANGO_SETTINGS_MODULE=config.settings.py

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]