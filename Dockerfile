FROM python:3.11.2-slim-bullseye
LABEL maintainer="contact@dmdhrumilmistry.tech"

# change working directory
WORKDIR /elb-log-analyzer

# upgrade pip
RUN pip install -U pip

# install tool
RUN pip install elb-log-analyzer
