@echo off
chcp 65001 > nul
echo.
echo 🐳 Docker Android APK构建脚本
echo ================================================
echo.

echo 📦 构建Docker镜像...
docker build -t ai-news-android .

if %errorlevel% neq 0 (
    echo ❌ Docker镜像构建失败
    pause
    exit /b 1
)

echo 🏗️ 在Docker容器中构建APK...
docker run --rm -v "%cd%\bin:/app/bin" ai-news-android

if %errorlevel% equ 0 (
    echo ✅ APK构建完成！
    echo 📁 APK文件位置: .\bin\
    dir bin\*.apk 2>nul
) else (
    echo ❌ APK构建失败
)

echo.
pause