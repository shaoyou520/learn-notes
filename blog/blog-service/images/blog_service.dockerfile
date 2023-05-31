from centos
run mkdir /root/.ssh && chmod 700 /root/.ssh
copy id_rsa /root/.ssh/
copy id_rsa.pub /root/.ssh/
copy apache-maven-3.8.8-bin.tar.gz /opt/maven/apache-maven-3.8.8-bin.tar.gz
copy jdk-8u211-linux-x64.tar.gz /opt/jdk-8u211-linux-x64.tar.gz

RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-* &&\
    sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*  &&\
    chmod 400 ~/.ssh/id_rsa &&\
    chmod 640 ~/.ssh/id_rsa.pub &&\
    echo 'StrictHostKeyChecking no' > ~/.ssh/config

RUN yum -y install git openssl wget nginx
COPY picture_nginx.conf /etc/nginx/nginx.conf

RUN cd /opt/maven && \
    tar -zxvf  apache-maven-3.8.8-bin.tar.gz &&\
    mv apache-maven-3.8.8/* /opt/maven/ &&\
    rm -rf apache-maven-3.8.8 apache-maven-3.8.8-bin.tar.gz &&\
    cd /opt && tar -zxvf jdk-8u211-linux-x64.tar.gz

COPY settings.xml /opt/maven/conf/settings.xml

ENV MAVEN_HOME=/opt/maven
ENV JAVA_HOME=/opt/jdk1.8.0_211
ENV PATH=$PATH:$JAVA_HOME/bin:$MAVEN_HOME/bin

RUN cd /root && mkdir code && cd code && \
    git clone git@github.com:shaoyou520/sy_statistics_service.git &&\
    cd sy_statistics_service && git config pull.ff only

RUN cd /root/code/sy_statistics_service && git pull && mvn clean install

WORKDIR /root/code/sy_statistics_service

ENTRYPOINT ["nginx"]
