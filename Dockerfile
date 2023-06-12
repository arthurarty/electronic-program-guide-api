# syntax=docker/dockerfile:1 
FROM python:3.10.12

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /usr/src/app
COPY . .
RUN apt-get update -y
RUN apt-get install -y iputils-ping
RUN pip install -r requirements.txt
RUN echo "1" | apt-get install  -yq mono-complete
RUN .wg++/install.sh
