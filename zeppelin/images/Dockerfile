FROM ubuntu:20.04

LABEL maintainer="Apache Software Foundation <dev@zeppelin.apache.org>"

ENV Z_VERSION="0.11.0"

ENV LOG_TAG="[ZEPPELIN_${Z_VERSION}]:" \
    ZEPPELIN_HOME="/opt/zeppelin" \
    HOME="/opt/zeppelin" \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 \
    ZEPPELIN_ADDR="0.0.0.0" \
    HADOOP_HOME="" \
    PATH=$PATH:$HADOOP_HOME/bin

RUN echo "$LOG_TAG install basic packages" && \
    apt-get -y update && \
    # Switch back to install JRE instead of JDK when moving to JDK9 or later.
    DEBIAN_FRONTEND=noninteractive apt-get install -y --fix-missing \
    net-tools curl vim locales language-pack-en tini openjdk-8-jdk-headless openjdk-8-jre-headless wget unzip && \
    # Cleanup
    rm -rf /var/lib/apt/lists/* && \
    apt-get autoclean && \
    apt-get clean

COPY zeppelin-0.11.0-SNAPSHOT.tar.gz /tmp/zeppelin-0.11.0-SNAPSHOT.tar.gz

RUN mkdir -p ${ZEPPELIN_HOME} && \
    tar --strip-components=1 -zxf  /tmp/zeppelin-0.11.0-SNAPSHOT.tar.gz -C ${ZEPPELIN_HOME} && \
    rm -f /tmp/zeppelin-0.11.0-SNAPSHOT.tar.gz &&\
    chown -R root:root ${ZEPPELIN_HOME} && \
    mkdir -p ${ZEPPELIN_HOME}/logs ${ZEPPELIN_HOME}/run ${ZEPPELIN_HOME}/webapps
    # Allow process to edit /etc/passwd, to create a user entry for zeppelin

COPY log4j.properties ${ZEPPELIN_HOME}/conf/
COPY log4j_docker.properties ${ZEPPELIN_HOME}/conf/
COPY log4j2.properties ${ZEPPELIN_HOME}/conf/
COPY log4j2_docker.properties ${ZEPPELIN_HOME}/conf/


EXPOSE 8080

ENTRYPOINT [ "/usr/bin/tini", "--" ]
WORKDIR ${ZEPPELIN_HOME}
CMD ["bin/zeppelin.sh"]
