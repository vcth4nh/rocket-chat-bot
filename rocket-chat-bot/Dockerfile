FROM python:3.10.16-alpine3.21

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY ./rocketchat-async /rocketchat-async
WORKDIR /rocketchat-async
RUN python setup.py install

COPY ./detect-secrets /detect-secrets
WORKDIR /detect-secrets
RUN python setup.py install

WORKDIR /app