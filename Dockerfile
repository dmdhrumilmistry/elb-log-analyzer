FROM python:3.11.2-slim-bullseye
LABEL maintainer="contact@dmdhrumilmistry.tech"

# change working directory
WORKDIR /elb-log-analyzer

# upgrade pip
RUN pip install -U pip

# install tool
RUN pip install elb-log-analyzer

# create logs dir
RUN mkdir -p /elb-log-analyzer/logs/latest
RUN mkdir -p /elb-log-analyzer/analyzed_logs


# copy workflow bashscript to /elb-log-analyzer
COPY ./docker-workflow.sh /elb-log-analyzer/workflow.sh

ENTRYPOINT ["/bin/bash", "/elb-log-analyzer/workflow.sh"]
