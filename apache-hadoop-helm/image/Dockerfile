FROM centos:8

COPY jdk-8u211-linux-x64.tar.gz /opt/jdk-8u211-linux-x64.tar.gz

ENV HADOOP_VERSION 3.3.5
ENV HADOOP_HOME=/opt/hadoop

ENV HADOOP_COMMON_HOME=${HADOOP_HOME} \
    HADOOP_HDFS_HOME=${HADOOP_HOME} \
    HADOOP_MAPRED_HOME=${HADOOP_HOME} \
    HADOOP_YARN_HOME=${HADOOP_HOME} \
    HADOOP_CONF_DIR=${HADOOP_HOME}/etc/hadoop \
    PATH=${PATH}:${HADOOP_HOME}/bin

RUN cd /opt && tar -zxvf jdk-8u211-linux-x64.tar.gz &&\
    curl --silent --output /tmp/hadoop.tgz \
    https://ftp-stud.hs-esslingen.de/pub/Mirrors/ftp.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz \
    && tar --directory /opt -xzf /tmp/hadoop.tgz \
    && rm /tmp/hadoop.tgz

ENV JAVA_HOME=/opt/jdk1.8.0_211
ENV PATH=$PATH:$JAVA_HOME/bin

RUN ln -s /opt/hadoop-${HADOOP_VERSION} ${HADOOP_HOME}

WORKDIR $HADOOP_HOME

# Hdfs ports
EXPOSE 50010 50020 50070 50075 50090 8020 9000

# Mapred ports
EXPOSE 19888

#Yarn ports
EXPOSE 8030 8031 8032 8033 8040 8042 8088

#Other ports
EXPOSE 49707 2122
