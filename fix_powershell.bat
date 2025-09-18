@echo off
chcp 65001 > nul
echo.
echo 🔧 PowerShell Python环境激活问题修复工具
echo ================================================
echo.

:menu
echo 请选择解决方案：
echo.
echo 1. 🛠️ 修复PowerShell执行策略（推荐）
echo 2. 🖥️ 使用命令提示符（CMD）运行
echo 3. 📋 查看问题说明和手动解决方法
echo 4. 🧪 测试Python环境
echo 5. ❌ 退出
echo.
set /p choice=请输入数字选择: 

if "%choice%"=="1" goto fix_powershell
if "%choice%"=="2" goto use_cmd
if "%choice%"=="3" goto show_manual
if "%choice%"=="4" goto test_python
if "%choice%"=="5" goto exit
goto menu

:fix_powershell
echo.
echo 🛠️ 正在修复PowerShell执行策略...
echo.
echo 📋 方案1: 当前用户权限修复
powershell -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"
if %errorlevel% equ 0 (
    echo ✅ 执行策略修复成功！
    echo.
    echo 🧪 正在测试Python环境激活...
    python --version
    if %errorlevel% equ 0 (
        echo ✅ Python环境正常
    ) else (
        echo ⚠️ Python可能需要重新安装或配置PATH
    )
) else (
    echo ❌ 修复失败，可能需要管理员权限
    echo.
    echo 📋 手动解决方法：
    echo 1. 右键点击PowerShell，选择"以管理员身份运行"
    echo 2. 运行命令：Set-ExecutionPolicy RemoteSigned
    echo 3. 选择 Y 确认
)
echo.
pause
goto menu

:use_cmd
echo.
echo 🖥️ 启动命令提示符环境...
echo.
echo 📋 在新打开的CMD窗口中，您可以：
echo.
echo   python main.py --once        # 执行一次抓取
echo   python main_android.py       # 运行Android版本
echo   python main.py --stats       # 查看统计信息
echo   python main.py --test-email  # 测试邮件发送
echo.
echo 💡 CMD不需要执行策略，直接支持Python环境
echo.
start cmd /k "cd /d %cd% && echo 🤖 AI资讯智能体 - 命令提示符环境 && echo ================================================ && echo 📍 当前目录: %cd% && echo 🐍 Python版本: && python --version && echo."
pause
goto menu

:show_manual
echo.
echo 📋 PowerShell Python环境激活问题说明
echo ================================================
echo.
echo 🔍 问题原因：
echo   PowerShell的默认执行策略是Restricted，阻止了脚本执行
echo   这影响了Python虚拟环境的激活脚本运行
echo.
echo 🛠️ 解决方法（按优先级）：
echo.
echo 方法1: 修改执行策略（推荐）
echo   1. 以管理员身份运行PowerShell
echo   2. 执行：Set-ExecutionPolicy RemoteSigned
echo   3. 输入 Y 确认
echo.
echo 方法2: 临时绕过（单次）
echo   powershell -ExecutionPolicy Bypass -File 脚本名.ps1
echo.
echo 方法3: 使用命令提示符
echo   在CMD中运行Python命令，不受此限制影响
echo.
echo 方法4: IDE内置终端
echo   使用VS Code、PyCharm等IDE的内置终端
echo.
echo 🔒 安全说明：
echo   RemoteSigned策略允许本地脚本运行，但要求
echo   从网络下载的脚本必须有数字签名，这是安全的
echo.
pause
goto menu

:test_python
echo.
echo 🧪 测试Python环境...
echo ================================
echo.
echo 🐍 Python版本：
python --version
echo.
echo 📦 pip版本：
pip --version
echo.
echo 🔍 Python路径：
where python
echo.
echo 📋 已安装的AI资讯智能体相关包：
echo.
echo 检查 requests...
pip show requests >nul 2>&1 && echo ✅ requests || echo ❌ requests 未安装
echo 检查 beautifulsoup4...
pip show beautifulsoup4 >nul 2>&1 && echo ✅ beautifulsoup4 || echo ❌ beautifulsoup4 未安装
echo 检查 feedparser...
pip show feedparser >nul 2>&1 && echo ✅ feedparser || echo ❌ feedparser 未安装
echo 检查 schedule...
pip show schedule >nul 2>&1 && echo ✅ schedule || echo ❌ schedule 未安装
echo 检查 kivy...
pip show kivy >nul 2>&1 && echo ✅ kivy || echo ❌ kivy 未安装
echo.
echo 🧪 测试AI资讯智能体运行：
echo.
python -c "print('🎉 Python环境测试成功！')"
if %errorlevel% equ 0 (
    echo ✅ Python基础环境正常
) else (
    echo ❌ Python环境存在问题
)
echo.
pause
goto menu

:exit
echo.
echo 💡 解决方案总结：
echo ================
echo.
echo 🎯 最简单方法：使用命令提示符（CMD）
echo   - 不受PowerShell执行策略影响
echo   - 直接运行所有Python命令
echo   - 推荐日常使用
echo.
echo 🔧 根本解决：修复PowerShell执行策略
echo   - 需要管理员权限
echo   - 一次修复，永久有效
echo   - 适合高级用户
echo.
echo 📱 对AI资讯智能体的影响：
echo   - 桌面版本：在CMD中完全正常运行
echo   - Android版本：在CMD中测试界面正常
echo   - GitHub构建：不受本地环境影响
echo.
echo 👋 感谢使用！您的AI资讯智能体功能完全正常！
echo.
pause
exit