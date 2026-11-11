FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$JAVA_HOME/bin

RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jdk-headless \
    python3 \
    python3-pip \
    openssh-server \
    openssh-client \
    curl \
    rsync \
    && rm -rf /var/lib/apt/lists/*

# Descargar e instalar Hadoop
RUN curl -sL https://archive.apache.org/dist/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz | tar -xz -C /opt/ \
    && mv /opt/hadoop-3.3.6 $HADOOP_HOME

# Configurar SSH sin contraseña para root
RUN mkdir -p /var/run/sshd /root/.ssh && \
    ssh-keygen -t rsa -P "" -f /root/.ssh/id_rsa && \
    cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys && \
    chmod 600 /root/.ssh/authorized_keys && \
    chmod 700 /root/.ssh

# Configurar SSH para no pedir confirmación de host
RUN echo "Host *\n  StrictHostKeyChecking no\n  UserKnownHostsFile=/dev/null\n" >> /root/.ssh/config

# Cargar variables de entorno globalmente para sesiones SSH no interactivas
RUN echo "export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64" >> /etc/profile && \
    echo "export HADOOP_HOME=/opt/hadoop" >> /etc/profile && \
    echo "export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin:\$JAVA_HOME/bin" >> /etc/profile && \
    echo "export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64" >> /root/.bashrc && \
    echo "export HADOOP_HOME=/opt/hadoop" >> /root/.bashrc && \
    echo "export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin:\$JAVA_HOME/bin" >> /root/.bashrc && \
    echo "PermitUserEnvironment yes" >> /etc/ssh/sshd_config && \
    echo "JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64\nHADOOP_HOME=/opt/hadoop\nPATH=$PATH:/opt/hadoop/bin:/opt/hadoop/sbin:/usr/lib/jvm/java-17-openjdk-amd64/bin" > /root/.ssh/environment

WORKDIR /app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 22

ENTRYPOINT ["/entrypoint.sh"]
CMD ["tail", "-f", "/dev/null"]