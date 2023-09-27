from kafka import KafkaProducer
import os

#9092:32452/TCP
producer = KafkaProducer(bootstrap_servers=os.environ.get('KAFKA_HOST', 'node1:32452'))
future = producer.send('test', key=b'my_key', value=b'my_value', partition=0)
result = future.get(timeout=100)
print(result)

