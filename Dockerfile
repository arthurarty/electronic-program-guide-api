# syntax=docker/dockerfile:1 
FROM python:3.10.12

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /usr/src/app
COPY . .
RUN apt-get update
RUN echo "1" | apt-get install  -yq mono-complete
RUN .wg++/install.sh
CMD ["bash"]
