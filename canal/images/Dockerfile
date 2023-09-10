from centos:8

ENV version=1.1.6

RUN sed -i -e "s|mirrorlist=|#mirrorlist=|g" /etc/yum.repos.d/CentOS-* \
    && sed -i -e "s|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g" /etc/yum.repos.d/CentOS-* \
    && yum update -y && yum install java-11-openjdk-devel -y \
    && yum install java-11-openjdk wget unzip net-tools -y

RUN wget https://github.com/alibaba/canal/releases/download/canal-$version/canal.deployer-$version.tar.gz \
    && mkdir /opt/canal && tar -zxf canal.deployer-$version.tar.gz  -C /opt/canal \
    && rm -f canal.deployer-$version.tar.gz \
    && wget https://github.com/alibaba/canal/releases/download/canal-$version/canal.admin-$version.tar.gz \
    && mkdir /opt/canal-admin \
    && tar -zxf canal.admin-$version.tar.gz  -C /opt/canal-admin \
    && rm -f canal.admin-$version.tar.gz
