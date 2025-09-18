# Android APK构建Docker容器
FROM ubuntu:22.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV ANDROID_HOME=/opt/android-sdk
ENV PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:$JAVA_HOME/bin

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    git zip unzip curl wget \
    openjdk-17-jdk \
    autoconf libtool pkg-config \
    zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 \
    cmake libffi-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装Python构建工具
RUN pip3 install buildozer cython

# 创建工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 设置构建脚本权限
RUN chmod +x /app/build_docker.sh

# 暴露构建目录
VOLUME ["/app/bin"]

# 默认命令
CMD ["bash", "/app/build_docker.sh"]