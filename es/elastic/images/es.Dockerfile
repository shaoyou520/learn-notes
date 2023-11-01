FROM centos:8

RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-* &&\
    sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*  &&\
    adduser elasticsearch &&\
    yum install wget curl net-tools perl-Digest-SHA -y

RUN cd /opt &&\
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.10.4-linux-x86_64.tar.gz &&\
    tar -xzf elasticsearch-8.10.4-linux-x86_64.tar.gz &&\
    chown -R elasticsearch elasticsearch-8.10.4 &&\
    rm -f elasticsearch-8.10.4-linux-x86_64.tar.gz

USER elasticsearch

CMD ['/opt/elasticsearch-8.10.4/bin/elasticsearch']