# 文件准备
### CA证书配置

#### master_ssl.cnf
```
[req]
req_extensions = v3_req
distinguished_name = req_distinguished_name
[req_distinguished_name]

[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = kubernetes
DNS.2 = kubernetes.default
DNS.3 = kubernetes.default.svc
DNS.4 = kubernetes.default.svc.cluster.local
DNS.5 = node1
DNS.6 = node2
DNS.7 = node3
DNS.8 = node4
DNS.9 = master
IP.1 = 182.43.15.195
IP.2 = 182.43.15.51
IP.3 = 182.43.110.62
IP.4 = 182.43.50.112
IP.5 = 10.0.0.210
IP.6 = 10.0.1.152
IP.7 = 10.0.1.207
IP.8 = 10.0.3.54
IP.9 = 10.100.0.1
```
### 创建服务端CA证书

openssl genrsa -out apiserver.key 2048
openssl req -new -key apiserver.key -config master_ssl.cnf -subj "/CN=master" -out apiserver.csr
openssl x509 -req -in apiserver.csr -CA ca.crt -CAkey ca.key -CAcreateserial -days 36500 -extensions v3_req -extfile master_ssl.cnf -out apiserver.crt


# kube-apiservice

## Kubernetes各服务的配置

### /usr/lib/systemd/system/kube-apiserver.service
```
[Unit]
Description=Kubernetes API Server
Documentation=https://github.com/kubernetes/kubernetes

[Service]
EnvironmentFile=/etc/kubernetes/apiserver
ExecStart=/usr/bin/kube-apiserver $KUBE_API_ARGS
Restart=always

[Install]
WantedBy=multi-user.target
```


### /etc/kubernetes/apiserver
```
KUBE_API_ARGS="--secure-port=6443 \
--tls-cert-file=/etc/kubernetes/pki/apiserver.crt \
--tls-private-key-file=/etc/kubernetes/pki/apiserver.key \
--client-ca-file=/etc/kubernetes/pki/ca.crt \
--apiserver-count=1 --endpoint-reconciler-type=master-count \
--etcd-servers=https://10.0.1.207:2379 \
--etcd-cafile=/etc/kubernetes/pki/ca.crt \
--etcd-certfile=/etc/kubernetes/pki/etcd_client.crt \
--etcd-keyfile=/etc/kubernetes/pki/etcd_client.key \
--service-cluster-ip-range=10.100.0.0/16 \
--service-node-port-range=30000-32767 \
--allow-privileged=true \
--advertise-address=182.43.110.62 \
--service-account-issuer=https://kubernetes.service.account.issuer \
--service-account-signing-key-file=/etc/kubernetes/pki/apiserver.key \
--service-account-key-file=/etc/kubernetes/pki/apiserver.crt \
--v=0"


systemctl status kube-apiserver
systemctl restart kube-apiserver && systemctl enable kube-apiserver
```
# 客户端访问证书及配置文件

### 创建客户端CA证书
```
openssl genrsa -out client.key 2048
openssl req -new -key client.key -subj "/CN=admin" -out client.csr
openssl x509 -req -in client.csr -CA ca.crt -CAkey /etc/kubernetes/pki/ca.key -CAcreateserial -out client.crt -days 36500
```

### /etc/kubernetes/kubeconfig
```
apiVersion: v1
kind: Config
clusters:
- name: default
  cluster:
    server: https://10.0.1.207:6443
    certificate-authority: /etc/kubernetes/pki/ca.crt
users:
- name: admin
  user:
    client-certificate: /etc/kubernetes/pki/client.crt
    client-key: /etc/kubernetes/pki/client.key
contexts:
- context:
    cluster: default
    user: admin
  name: default
current-context: default
```

## kube-controller-manage
```
# /usr/lib/systemd/system/kube-controller-manager.service
[Unit]
Description=Kubernetes Controller Manager
Documentation=https://github.com/kubernetes/kubernetes

[Service]
EnvironmentFile=/etc/kubernetes/controller-manager
ExecStart=/usr/bin/kube-controller-manager $KUBE_CONTROLLER_MANAGER_ARGS
Restart=always

[Install]
WantedBy=multi-user.target


# /etc/kubernetes/controller-manager
KUBE_CONTROLLER_MANAGER_ARGS="--kubeconfig=/etc/kubernetes/kubeconfig \
--leader-elect=false \
--service-cluster-ip-range=10.100.0.0/16 \
--service-account-private-key-file=/etc/kubernetes/pki/apiserver.key \
--root-ca-file=/etc/kubernetes/pki/ca.crt \
--v=0"

systemctl status kube-controller-manager
systemctl restart kube-controller-manager && systemctl enable kube-controller-manager

```

## kube-scheduler
```
# /usr/lib/systemd/system/kube-scheduler.service
[Unit]
Description=Kubernetes Scheduler
Documentation=https://github.com/kubernetes/kubernetes

[Service]
EnvironmentFile=/etc/kubernetes/scheduler
ExecStart=/usr/bin/kube-scheduler $KUBE_SCHEDULER_ARGS
Restart=always

[Install]
WantedBy=multi-user.target


# /etc/kubernetes/scheduler
KUBE_SCHEDULER_ARGS="--kubeconfig=/etc/kubernetes/kubeconfig \
--leader-elect=true \
--v=0"

systemctl status kube-scheduler
systemctl restart kube-scheduler && systemctl enable kube-scheduler


```

