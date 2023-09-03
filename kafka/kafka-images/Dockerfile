FROM ubuntu:16.04

ENV KAFKA_HOME /usr/local/kafka
ADD ./start-kafka.sh /scripts/

# install java + others
RUN apt-get update && apt-get install -y wget openjdk-8-jdk \
    && chmod 750 /scripts/start-kafka.sh

# install kafka
RUN wget http://apache.cs.utah.edu/kafka/3.5.1/kafka_2.12-3.5.1.tgz && \
  tar -xzf kafka_2.12-3.5.1.tgz && \
  mv kafka_2.12-3.5.1 $KAFKA_HOME

CMD ["/scripts/start-kafka.sh"]