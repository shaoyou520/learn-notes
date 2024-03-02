## 文件准备
etcd-v3.4.24-linux-amd64解压etcdctl，etcd

## 生成CA根证书
```
cd /etc/kubernetes/pki
openssl genrsa -out ca.key 2048
openssl req -x509 -new -nodes -key ca.key -subj "/CN=master" -days 36500 -out ca.crt
```

## 根据根证书颁发证书
vi etcd_ssl.cnf
```
[ req ]
req_extensions = v3_req
distinguished_name = req_distinguished_name

[ req_distinguished_name ]

[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names

[ alt_names ]
IP.1 = 182.43.15.195
IP.2 = 182.43.15.51
IP.3 = 182.43.110.62
IP.4 = 182.43.50.112
IP.5 = 10.0.0.210
IP.6 = 10.0.1.152
IP.7 = 10.0.1.207
IP.7 = 10.0.3.54
```

```
openssl genrsa -out etcd_server.key 2048
openssl req -new -key etcd_server.key -config etcd_ssl.cnf -subj "/CN=etcd-server" -out etcd_server.csr
openssl x509 -req -in etcd_server.csr -CA /etc/kubernetes/pki/ca.crt -CAkey /etc/kubernetes/pki/ca.key -CAcreateserial -days 36500 -extensions v3_req -extfile etcd_ssl.cnf -out etcd_server.crt

openssl genrsa -out etcd_client.key 2048
openssl req -new -key etcd_client.key -config etcd_ssl.cnf -subj "/CN=etcd_client" -out etcd_client.csr
openssl x509 -req -in etcd_client.csr -CA /etc/kubernetes/pki/ca.crt -CAkey /etc/kubernetes/pki/ca.key -CAcreateserial -days 36500 -extensions v3_req -extfile etcd_ssl.cnf -out etcd_client.crt

```

## 设置成systemd服务：
`vi /usr/lib/systemd/system/etcd.service`

```
[Unit]
Description=etcd key-value store
Documentation=https://github.com/etcd-io/etcd
After=network.target

[Service]
EnvironmentFile=/etc/etcd/etcd.conf
ExecStart=/usr/bin/etcd
Restart=always

[Install]
WantedBy=multi-user.target
```

`vi /etc/etcd/etcd.conf`

```
ETCD_NAME=etcd1
ETCD_DATA_DIR=/etc/etcd/data

ETCD_CERT_FILE=/etc/kubernetes/pki/etcd_server.crt
ETCD_KEY_FILE=/etc/kubernetes/pki/etcd_server.key
ETCD_TRUSTED_CA_FILE=/etc/kubernetes/pki/ca.crt
ETCD_CLIENT_CERT_AUTH=true
ETCD_LISTEN_CLIENT_URLS=https://10.0.1.207:2379
ETCD_ADVERTISE_CLIENT_URLS=https://10.0.1.207:2379

ETCD_PEER_CERT_FILE=/etc/kubernetes/pki/etcd_server.crt
ETCD_PEER_KEY_FILE=/etc/kubernetes/pki/etcd_server.key
ETCD_PEER_TRUSTED_CA_FILE=/etc/kubernetes/pki/ca.crt
ETCD_LISTEN_PEER_URLS=https://10.0.1.207:2380
# 单节点下面不用
ETCD_INITIAL_ADVERTISE_PEER_URLS=https://10.0.1.207:2380

ETCD_INITIAL_CLUSTER_TOKEN=etcd-cluster
ETCD_INITIAL_CLUSTER="etcd1=https://10.0.1.207:2380"
ETCD_INITIAL_CLUSTER_STATE=new
```

## 启动
`systemctl restart etcd && systemctl enable etcd`
## 查看状态
`systemctl status etcd`

## 语法：
```
etcdctl --cacert=/etc/kubernetes/pki/ca.crt \
--cert=/etc/kubernetes/pki/etcd_client.crt \
--key=/etc/kubernetes/pki/etcd_client.key \
--endpoints=https://182.43.110.62:2379 endpoint health


etcdctl --cacert=/etc/kubernetes/pki/ca.crt \
--cert=/etc/etcd/pki/etcd_client.crt \
--key=/etc/etcd/pki/etcd_client.key \
--endpoints=https://82.43.110.62:2379 endpoint health


etcdctl --cacert=/etc/kubernetes/pki/ca.crt \
--cert=/etc/etcd/pki/etcd_client.crt \
--key=/etc/etcd/pki/etcd_client.key \
--endpoints=https://82.43.110.62:2379 get /coreos.com/network/subnets/

etcdctl \
--endpoints=https://10.0.0.210:2379 \
--cacert=/etc/kubernetes/pki/ca.crt \
--cert=/etc/kubernZetes/pki/client.crt \
--key=/etc/kubernetes/pki/client.key \
get / --prefix --keys-only
```