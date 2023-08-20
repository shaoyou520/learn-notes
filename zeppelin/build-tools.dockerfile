from ubuntu:20.04

copy apache-maven-3.8.8-bin.tar.gz /opt/maven/apache-maven-3.8.8-bin.tar.gz
copy jdk-8u211-linux-x64.tar.gz /opt/jdk-8u211-linux-x64.tar.gz

RUN cd /opt/maven && \
    tar -zxvf  apache-maven-3.8.8-bin.tar.gz &&\
    mv apache-maven-3.8.8/* /opt/maven/ &&\
    rm -rf apache-maven-3.8.8 apache-maven-3.8.8-bin.tar.gz &&\
    cd /opt && tar -zxvf jdk-8u211-linux-x64.tar.gz

ENV MAVEN_HOME=/opt/maven
ENV JAVA_HOME=/opt/jdk1.8.0_211
ENV PATH=$PATH:$JAVA_HOME/bin:$MAVEN_HOME/bin

RUN cd /root && mkdir code && cd code

