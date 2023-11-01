FROM centos:8

RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-* &&\
    sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*  &&\
    yum install wget curl net-tools perl-Digest-SHA -y

RUN curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.10.4-linux-x86_64.tar.gz &&\
    tar xzvf filebeat-8.10.4-linux-x86_64.tar.gz &&\
    rm -rf filebeat-8.10.4-linux-x86_64.tar.gz

CMD ['./filebeat -e']