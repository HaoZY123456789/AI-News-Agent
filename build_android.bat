@echo off
chcp 65001 > nul
echo.
echo 🤖 AI资讯智能体 - Android APK 构建脚本
echo ================================================
echo.

:menu
echo 请选择操作：
echo 1. 🧪 桌面测试 Android 版本
echo 2. 🏗️ 构建调试版 APK
echo 3. 📦 构建发布版 APK
echo 4. 🧹 清理构建缓存
echo 5. 📊 查看构建状态
echo 6. ❌ 退出
echo.
set /p choice=请输入数字选择: 

if "%choice%"=="1" goto test_desktop
if "%choice%"=="2" goto build_debug
if "%choice%"=="3" goto build_release
if "%choice%"=="4" goto clean_build
if "%choice%"=="5" goto check_status
if "%choice%"=="6" goto exit
goto menu

:test_desktop
echo.
echo 🧪 启动桌面测试版本...
echo ⚠️  注意：这是Android界面的桌面预览版本
echo.
python main_android.py
echo.
pause
goto menu

:build_debug
echo.
echo 🏗️ 开始构建调试版 APK...
echo ⏰ 首次构建可能需要 30-60 分钟
echo.
buildozer android debug
if %errorlevel% equ 0 (
    echo ✅ 调试版 APK 构建成功！
    echo 📁 文件位置: .\bin\aiNewsAgent-1.0-armeabi-v7a-debug.apk
) else (
    echo ❌ 构建失败，请检查错误信息
)
echo.
pause
goto menu

:build_release
echo.
echo 📦 开始构建发布版 APK...
echo ⚠️  发布版需要更长时间，并且需要签名
echo.
buildozer android release
if %errorlevel% equ 0 (
    echo ✅ 发布版 APK 构建成功！
    echo 📁 文件位置: .\bin\aiNewsAgent-1.0-armeabi-v7a-release.apk
) else (
    echo ❌ 构建失败，请检查错误信息
)
echo.
pause
goto menu

:clean_build
echo.
echo 🧹 清理构建缓存...
buildozer android clean
echo ✅ 缓存清理完成
echo.
pause
goto menu

:check_status
echo.
echo 📊 构建状态检查
echo ================================================
echo.
echo 📁 项目文件检查：
if exist "buildozer.spec" (
    echo ✅ buildozer.spec 配置文件存在
) else (
    echo ❌ buildozer.spec 配置文件不存在
)

if exist "main_android.py" (
    echo ✅ main_android.py 主程序存在
) else (
    echo ❌ main_android.py 主程序不存在
)

echo.
echo 📦 输出文件检查：
if exist "bin" (
    echo ✅ bin 目录存在
    dir bin\*.apk /b 2>nul | find /c /v "" > temp_count.txt
    set /p apk_count=<temp_count.txt
    del temp_count.txt
    echo 📱 发现 %apk_count% 个 APK 文件
    if exist "bin\*.apk" (
        echo 📁 APK 文件列表：
        dir bin\*.apk /b
    )
) else (
    echo ❌ bin 目录不存在（尚未构建）
)

echo.
echo 🔧 依赖检查：
python -c "import kivy; print('✅ Kivy:', kivy.__version__)" 2>nul || echo ❌ Kivy 未安装
python -c "import kivymd; print('✅ KivyMD 已安装')" 2>nul || echo ❌ KivyMD 未安装
where buildozer >nul 2>&1 && echo ✅ Buildozer 已安装 || echo ❌ Buildozer 未安装

echo.
pause
goto menu

:exit
echo.
echo 👋 感谢使用 AI资讯智能体 Android 构建工具！
echo 🚀 祝您的 Android 应用运行顺利！
echo.
pause
exit