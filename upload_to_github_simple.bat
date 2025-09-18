@echo off
rem 设置UTF-8编码
chcp 65001 >nul

echo.
echo AI资讯智能体 - GitHub上传工具
echo =======================================
echo.

:menu
echo 请选择操作：
echo.
echo 1. 初始化Git仓库
echo 2. 上传到GitHub（首次）
echo 3. 更新代码到GitHub
echo 4. 打开GitHub Actions页面
echo 5. 查看使用说明
echo 6. 退出
echo.
set /p choice=请输入数字选择: 

if "%choice%"=="1" goto init_git
if "%choice%"=="2" goto upload_github
if "%choice%"=="3" goto update_github
if "%choice%"=="4" goto open_actions
if "%choice%"=="5" goto show_guide
if "%choice%"=="6" goto exit
goto menu

:init_git
echo.
echo 正在初始化Git仓库...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：Git未安装，请先安装Git
    echo 下载地址：https://git-scm.com/
    pause
    goto menu
)

git init
if %errorlevel% equ 0 (
    echo 成功：Git仓库初始化完成
    git add .
    git commit -m "Initial commit: AI资讯智能体Android版本"
    echo 成功：初始提交完成
) else (
    echo 错误：Git初始化失败
)
echo.
pause
goto menu

:upload_github
echo.
echo 首次上传到GitHub...
echo.
echo 请确保您已在GitHub创建了新仓库
echo.
set /p repo_url=请输入GitHub仓库URL: 

if "%repo_url%"=="" (
    echo 错误：仓库URL不能为空
    pause
    goto menu
)

echo.
echo 开始上传...
git remote add origin %repo_url%
git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo 成功：代码上传完成！
    echo 信息：GitHub Actions将自动开始构建APK
    echo 时间：预计15-25分钟后APK构建完成
    echo.
    echo 查看构建进度：
    echo %repo_url%/actions
) else (
    echo 错误：上传失败，请检查：
    echo   - 网络连接
    echo   - GitHub仓库URL是否正确
    echo   - GitHub认证是否配置
)
echo.
pause
goto menu

:update_github
echo.
echo 更新代码到GitHub...
echo.
set /p commit_msg=请输入提交消息（回车使用默认）: 

if "%commit_msg%"=="" (
    set commit_msg=Update: 更新AI资讯智能体代码
)

git add .
git commit -m "%commit_msg%"
git push

if %errorlevel% equ 0 (
    echo 成功：代码更新完成！
    echo 信息：新的APK构建将自动开始
) else (
    echo 错误：更新失败，请检查网络连接和仓库状态
)
echo.
pause
goto menu

:open_actions
echo.
echo 正在打开GitHub Actions页面...
echo 如果浏览器没有自动打开，请手动访问：
echo https://github.com/您的用户名/您的仓库名/actions
echo.
start https://github.com
pause
goto menu

:show_guide
echo.
echo GitHub上传快速指南
echo ==================
echo.
echo 首次上传步骤：
echo 1. 在GitHub网站创建新仓库
echo 2. 运行本脚本选择"1. 初始化Git仓库"
echo 3. 选择"2. 上传到GitHub（首次）"
echo 4. 输入GitHub仓库URL
echo 5. 等待自动构建完成
echo.
echo 后续更新步骤：
echo 1. 修改代码后运行本脚本
echo 2. 选择"3. 更新代码到GitHub"
echo 3. 输入提交消息
echo 4. 等待自动构建完成
echo.
echo 下载APK：
echo 1. 访问GitHub仓库的Actions页面
echo 2. 选择最新的构建
echo 3. 下载Artifacts中的APK文件
echo.
echo 详细说明请查看：GitHub_Actions构建指南.md
echo.
pause
goto menu

:exit
echo.
echo 感谢使用AI资讯智能体GitHub自动构建工具！
echo.
echo 上传代码后，GitHub将自动构建您的Android APK
echo 访问：https://github.com/您的用户名/您的仓库名/actions
echo 详细指南：GitHub_Actions构建指南.md
echo.
pause
exit