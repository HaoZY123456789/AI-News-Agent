#!/bin/bash
# Docker容器内的构建脚本

echo "🤖 AI资讯智能体 - Docker Android构建"
echo "================================================"

# 设置Java路径
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$PATH:$JAVA_HOME/bin

echo "☕ Java版本检查:"
java -version

echo "🐍 Python版本检查:"
python3 --version

echo "🔧 Buildozer版本检查:"
buildozer --version

# 开始构建
echo "🏗️ 开始构建Android APK..."
buildozer android debug

if [ $? -eq 0 ]; then
    echo "✅ APK构建成功！"
    echo "📁 APK文件:"
    ls -la bin/*.apk 2>/dev/null || echo "未找到APK文件"
else
    echo "❌ APK构建失败"
    exit 1
fi