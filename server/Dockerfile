FROM tensorflow/tensorflow:2.1.0-py3 as builder

FROM builder

WORKDIR /usr/src

RUN pip3 install gunicorn

COPY ./requirements.txt .
RUN pip3 install  -r requirements.txt

RUN python -m spacy download es_core_news_md

COPY . .

ENV PYTHONUNBUFFERED=TRUE

CMD gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT wsgi:app --access-logfile=- --error-logfile=- --log-level=INFO