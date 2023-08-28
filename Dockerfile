# syntax=docker/dockerfile:1 
FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /usr/src/app
COPY . .
RUN apt-get clean
RUN apt-get update -y
RUN apt-get install -y iputils-ping
RUN apt-get install -yq dotnet-sdk-7.0
RUN apt-get install -yq ca-certificates && update-ca-certificates
RUN apt-get install -yq python3-pip
RUN pip3 install -r requirements.txt
RUN apt install -y git
RUN .wg++/install.sh
