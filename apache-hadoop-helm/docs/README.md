# Helm repo for Apache Hadoop
helm install my-hadoop apache-hadoop-helm/hadoop --version 1.2.0 --set image.repository=registry.cn-hangzhou.aliyuncs.com/qt1/hadoop --set image.tag=3.3.5 --set hdfs.dataNode.externalHostname=shaoyou.store
