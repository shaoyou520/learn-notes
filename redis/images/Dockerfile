FROM centos

RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-* &&\
    sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*

RUN yum update -y \
    && yum install wget gcc automake autoconf libtool make net-tools bind-utils -y \
    && cd /opt/ && wget http://download.redis.io/releases/redis-7.4.0.tar.gz \
    && tar -zxf redis-7.4.0.tar.gz \
    && rm -f redis-7.4.0.tar.gz \
    && cd redis-7.4.0 && make

ENV REDIS_HOME=/opt/redis-7.4.0
ENV PATH=$PATH:$REDIS_HOME/src
WORKDIR $REDIS_HOME


