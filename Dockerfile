# syntax=docker/dockerfile:1
   
FROM ubuntu:jammy
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /
COPY . .
RUN apt-get update
RUN echo "1" | apt-get install  -yq mono-complete
RUN apt-get install -yq wget
RUN wget http://webgrabplus.com/sites/default/files/download/SW/V3.3.0/WebGrabPlus_V3.3_install.tar.gz
RUN tar -zxvf WebGrabPlus_V3.3_install.tar.gz
RUN cd .wg++
CMD ["bash"]
