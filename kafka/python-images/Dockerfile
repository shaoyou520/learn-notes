FROM ubuntu:16.04

# install java + others
RUN apt update \
   &&  apt-get install -y wget zlib1g-dev  libbz2-dev libssl-dev libncurses5-dev libsqlite3-dev \
    python-dev libffi-dev make build-essential zlib1g-dev  libreadline-dev \
    curl llvm libncursesw5-dev xz-utils tk-dev \
    && wget https://www.python.org/ftp/python/3.9.13/Python-3.9.13.tgz \
    && tar -xf Python-3.9.13.tgz -C /opt/ \
    && cd /opt/Python-3.9.13 \
    && ./configure --prefix=/usr/local/python3 \
    && make && make install \
    && ln -s /usr/local/python3/bin/python3 /usr/bin/python3 \
    && ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3

