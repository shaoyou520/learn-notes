from kafka import KafkaProducer
import os
import sys

#9092:32452/TCP
producer = KafkaProducer(bootstrap_servers=os.environ.get('KAFKA_HOST', 'kafka-kafka-chats-'+sys.argv[1]+'.kafka-kafka-chats.default.svc.cluster.local:9093'))
print("------->>")
for i in range(5000):
    future = producer.send('test', key=b'my_key', value=b'my_valuesssssssiiiiinnnnnnnnnsmy_'
                                                        b'valuesssssssiiiiinnnnnnnnnsmy_value'
                                                        b'sssssssiiiiinnnnnnnnnsmy_valuesssssss'
                                                        b'iiiiinnnnnnnnnsmy_valuesssssssiiiiinnn'
                                                        b'nnnnnnsmy_valuesssssssiiiiinnnnnnnnnsmy_'
                                                        b'valuesssssssiiiiinnnnnnnnnsmy_valuesssssssii'
                                                        b'iiinnnnnnnnnsmy_valuesssssssiiiiinnnnnnnnnsmy_'
                                                        b'valuesssssssiiiiinnnnnnnnnsmy_valuesssssssiiiiinnn'
                                                        b'nnnnnnsmy_valuesssssssiiiiinnnnnnnnnsmy_valuesssssssi'
                                                        b'iiiinnnnnnnnnsmy_valuesssssssiiiiinnnnnnnnnsmy_valuesss'
                                                        b'ssssiiiiinnnnnnnnnsmy_valuesssssssiiiiinnnnnnnnnsmy_valu'
                                                        b'esssssssiiiiinnnnnnnnnsmy_valuesssssssiiiiinnnnnnnnnsmy_'
                                                        b'valuesssssssiiiiinnnnnnnnnsmy_valuesssssssiiiiinnnnnnnnnsmy_'
                                                        b'valuesssssssiiiiinnnnnnnnnsmy_valuesssssssiiiiinnnnnnnnnsmy_'
                                                        b'valuesssssssiiiiinnnnnnnnnsmy_valuesssssssiiiiinnnnnnnnnsmy_'
                                                        b'valuesssssssiiiiinnnnnnnnns', partition=0)
    result = future.get(timeout=100)
    print(result)

