from centos:8

RUN sed -i -e "s|mirrorlist=|#mirrorlist=|g" /etc/yum.repos.d/CentOS-* \
    && sed -i -e "s|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g" /etc/yum.repos.d/CentOS-* \
    && yum update -y && yum install java-11-openjdk-devel -y \
    && yum install java-11-openjdk wget git unzip net-tools -y

RUN cd /opt && mkdir zookeeper \
    && wget https://dlcdn.apache.org/zookeeper/zookeeper-3.9.0/apache-zookeeper-3.9.0-bin.tar.gz \
    && tar -zxf apache-zookeeper-3.9.0-bin.tar.gz \
    && rm -f apache-zookeeper-3.9.0-bin.tar.gz \
    && mv /opt/apache-zookeeper-3.9.0-bin/* /opt/zookeeper \
    && rm -rf /opt/apache-zookeeper-3.9.0-bin \
    && chown root:root /opt -R

CMD ["/opt/zookeeper/bin/zkServer.sh", "start-foreground"]
