FROM python:3.11.2-slim-bullseye
LABEL maintainer="contact@dmdhrumilmistry.tech"

WORKDIR /elb-log-analyzer
RUN pip install elb-log-analyzer
