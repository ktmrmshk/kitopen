FROM ubuntu:latest

RUN apt-get update \ 
    && apt-get install -y python3-pip python3-dev \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip \
    && apt-get install -y git \
    && pip3 install requests edgegrid-python

RUN git clone https://github.com/ktmrmshk/kitopen.git


