FROM ubuntu:16.04

ENV KAFKA_HOME /opt/kafka
ADD ./start-kafka.sh /scripts/

# install java + others
RUN apt-get update && apt-get install -y wget openjdk-8-jdk curl vim net-tools  \
    && chmod 750 /scripts/start-kafka.sh

# install kafka
COPY kafka_2.12-3.5.1.tgz /opt/
RUN cd /opt && tar -xzf kafka_2.12-3.5.1.tgz && \
  mv kafka_2.12-3.5.1 $KAFKA_HOME && rm -rf kafka_2.12-3.5.1.tgz

CMD ["/scripts/start-kafka.sh"]