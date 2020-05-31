FROM python:3.6.9

WORKDIR /usr/src

RUN pip install gunicorn

COPY ./requirements.txt .
RUN pip3 install  -r requirements.txt

RUN python -m spacy download es_core_news_md

COPY . .

CMD gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT wsgi:app