from centos
run mkdir /root/.ssh && chmod 700 /root/.ssh
copy id_rsa /root/.ssh/
copy id_rsa.pub /root/.ssh/

RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-* &&\
    sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*  &&\
    chmod 400 ~/.ssh/id_rsa &&\
    chmod 640 ~/.ssh/id_rsa.pub &&\
    echo 'StrictHostKeyChecking no' > ~/.ssh/config

RUN yum -y install nginx git openssl wget

RUN mkdir -p /opt/nodejs &&\
    cd /opt/nodejs &&\
    wget https://nodejs.org/dist/v18.16.0/node-v18.16.0-linux-x64.tar.xz &&\
    tar -xvf node-v18.16.0-linux-x64.tar.xz &&\
    mv node-v18.16.0-linux-x64/* ./ &&\
    ln -s /opt/nodejs/bin/node /usr/bin/node &&\
    ln -s /opt/nodejs/bin/npm /usr/bin/npm &&\
    rm -rf node-v18.16.0-linux-x64.tar.xz &&\
    rm -rf node-v18.16.0-linux-x64


RUN cd /root && mkdir code && cd code && \
    git clone git@github.com:shaoyou520/sy_blog.git &&\
    cd sy_blog  && git config pull.ff only

COPY blog_nginx.conf /etc/nginx/nginx.conf

RUN cd /root/code/sy_blog && npm instal

WORKDIR /root/code/sy_blog

CMD ["nginx", "-g", "daemon off;"]

