# 安装docker
```
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
systemctl daemon-reload
systemctl restart docker.service
systemctl enable docker.service
vi /etc/containerd/config.toml disabled_plugins删除cri
systemctl restart containerd
```

# 配置客户端访问文件
```
mkdir -p /etc/kubernetes/pki/
scp root@master:/etc/kubernetes/pki/ca.crt \
root@master:/etc/kubernetes/pki/client.crt \
root@master:/etc/kubernetes/pki/client.key /etc/kubernetes/pki/
```

### /etc/kubernetes/kubeconfig
```
apiVersion: v1
kind: Config
clusters:
- name: default
  cluster:
    server: https://182.43.110.62:6443
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
# kubelet
```
# /usr/lib/systemd/system/kubelet.service
[Unit]
Description=Kubernetes Kubelet Server
Documentation=https://github.com/kubernetes/kubernetes
After=docker.target

[Service]
EnvironmentFile=/etc/kubernetes/kubelet
ExecStart=/usr/bin/kubelet $KUBELET_ARGS
Restart=always

[Install]
WantedBy=multi-user.target


# /etc/kubernetes/kubelet
KUBELET_ARGS="--kubeconfig=/etc/kubernetes/kubeconfig \
--config=/etc/kubernetes/kubelet.config \
--hostname-override=node2 \
--pod-cidr=10.244.0.0/16 \
--container-runtime-endpoint=unix:///run/containerd/containerd.sock \
--v=0"


# /etc/kubernetes/kubelet.config
kind: KubeletConfiguration
apiVersion: kubelet.config.k8s.io/v1beta1
address: 0.0.0.0
port: 10250
cgroupDriver: cgroupfs
clusterDNS: ["10.100.0.100"]
clusterDomain: cluster.local
authentication:
  anonymous:
    enabled: true


systemctl status kubelet
systemctl restart kubelet && systemctl enable kubelet
```

# kube-proxy

```
# /usr/lib/systemd/system/kube-proxy.service
[Unit]
Description=Kubernetes Kube-Proxy Server
Documentation=https://github.com/kubernetes/kubernetes
After=network.target

[Service]
EnvironmentFile=/etc/kubernetes/proxy
ExecStart=/usr/bin/kube-proxy $KUBE_PROXY_ARGS
Restart=always

[Install]
WantedBy=multi-user.target



# /etc/kubernetes/proxy
KUBE_PROXY_ARGS="--kubeconfig=/etc/kubernetes/kubeconfig \
--hostname-override=node1 \
--proxy-mode=iptables \
--v=0"

systemctl status kube-proxy
systemctl restart kube-proxy && systemctl enable kube-proxy

```

# 配置kubectl， master and node
vi ~/.bash_profile
```
alias kubectl="/usr/bin/kubectl --kubeconfig=/etc/kubernetes/kubeconfig"
alias k=kubectl
alias kk="kubectl -n kube-system"
```
source ~/.bash_profile

# 跨vpc配置
```
master：
iptables -t nat -A OUTPUT -d 10.0.0.210 -j DNAT --to-destination 182.43.15.195
iptables -t nat -A OUTPUT -d 10.0.1.152 -j DNAT --to-destination 182.43.15.51
iptables -t nat -A OUTPUT -d 10.0.3.54 -j DNAT --to-destination 182.43.50.112

node：
iptables -t nat -A OUTPUT -d 10.0.1.207 -j DNAT --to-destination 182.43.110.62
```
问题：containerd 下载pause:3.6 镜像有问题
containerd config default > /etc/containerd/config.toml
修改 registry.k8s.io/pause:3.6 -> registry.aliyuncs.com/google_containers/pause:3.6
