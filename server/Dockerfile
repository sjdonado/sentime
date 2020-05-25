FROM tensorflow/tensorflow:2.1.0-py3 as builder

FROM builder

WORKDIR /usr/src

# RUN pip3 install wheel
# RUN pip3 install gunicorn

COPY ./requirements.txt .
RUN pip3 install  -r requirements.txt

RUN python -m spacy download es_core_news_md

COPY . .

# CMD ["gunicorn", "-b 0.0.0.0", "wsgi:app"]
CMD ["python3", "wsgi.py"]