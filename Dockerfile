FROM python:3.9-alpine

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps
RUN apk add libffi-dev
RUN apk update && apk add python3-dev \
    gcc \
    libc-dev
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8080

ENTRYPOINT ["python"]
CMD ["run.py"]