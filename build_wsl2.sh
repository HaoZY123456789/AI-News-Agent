#!/bin/bash
# WSL2 Android构建脚本
# 在WSL2 Ubuntu环境中运行此脚本

echo "🤖 AI资讯智能体 - WSL2 Android构建脚本"
echo "================================================"

# 更新系统
echo "📦 更新系统包..."
sudo apt update && sudo apt upgrade -y

# 安装必要依赖
echo "🔧 安装构建依赖..."
sudo apt install -y python3-pip python3-venv git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# 安装Android构建工具
echo "📱 安装Android构建工具..."
pip3 install --user buildozer cython

# 设置环境变量
echo "⚙️ 设置环境变量..."
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$PATH:~/.local/bin

# 进入项目目录（假设已经复制到WSL2）
cd /mnt/d/QoderProject

# 开始构建
echo "🏗️ 开始构建Android APK..."
buildozer android debug

echo "✅ 构建完成！"
echo "📁 APK位置: ./bin/"