FROM ubuntu:18.04

RUN apt-get update && apt-get install -y --no-install-recommends \
        sudo \
        git \
        build-essential \
        python-setuptools \
        libpq-dev\
        pgloader\
        cmake \
        wget \
        curl \
        libsm6 \
        libxext6 \
        libxrender-dev \
        vim


RUN apt-get update && apt-get install --no-install-recommends  -y python3.7 python3-pip
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1


RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools


RUN pip3 install grpcio
RUN pip3 install grpcio-tools
RUN pip3 install protobuf

RUN pip3 install pymysql

WORKDIR /SMART-BUS

COPY . /SMART-BUS



RUN sh buildproto.sh


CMD ["python3", "smart_bus.py"]

