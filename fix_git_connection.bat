@echo off
chcp 65001 >nul
echo.
echo Git连接问题修复工具
echo =======================
echo.

:menu
echo 请选择解决方案：
echo.
echo 1. 检查网络连接状态
echo 2. 修复Git HTTPS连接问题
echo 3. 配置Git代理设置
echo 4. 重新配置远程仓库
echo 5. 使用SSH方式连接
echo 6. 测试Git连接
echo 7. 查看详细错误信息
echo 8. 退出
echo.
set /p choice=请输入数字选择: 

if "%choice%"=="1" goto check_network
if "%choice%"=="2" goto fix_https
if "%choice%"=="3" goto config_proxy
if "%choice%"=="4" goto reconfig_remote
if "%choice%"=="5" goto setup_ssh
if "%choice%"=="6" goto test_connection
if "%choice%"=="7" goto show_error_info
if "%choice%"=="8" goto exit
goto menu

:check_network
echo.
echo 检查网络连接状态...
echo ====================
echo.
echo 测试GitHub连接：
ping -n 3 github.com
echo.
echo 测试DNS解析：
nslookup github.com
echo.
echo 检查Git配置：
git config --list | findstr -i http
echo.
pause
goto menu

:fix_https
echo.
echo 修复Git HTTPS连接问题...
echo =========================
echo.
echo 1. 禁用SSL证书验证（临时解决）
git config --global http.sslVerify false
echo 完成：已禁用SSL验证
echo.
echo 2. 增加HTTP缓冲区大小
git config --global http.postBuffer 524288000
echo 完成：已增加缓冲区大小
echo.
echo 3. 设置HTTP版本
git config --global http.version HTTP/1.1
echo 完成：已设置HTTP版本
echo.
echo 4. 增加超时时间
git config --global http.lowSpeedLimit 0
git config --global http.lowSpeedTime 999999
echo 完成：已增加超时时间
echo.
echo 修复完成！请尝试重新推送代码
pause
goto menu

:config_proxy
echo.
echo 配置Git代理设置...
echo =================
echo.
echo 当前代理设置：
git config --get http.proxy
git config --get https.proxy
echo.
echo 请选择代理配置：
echo 1. 清除代理设置
echo 2. 设置HTTP代理
echo 3. 返回主菜单
echo.
set /p proxy_choice=请选择: 

if "%proxy_choice%"=="1" (
    git config --global --unset http.proxy
    git config --global --unset https.proxy
    echo 已清除代理设置
) else if "%proxy_choice%"=="2" (
    set /p proxy_url=请输入代理地址（如：http://127.0.0.1:8080）: 
    git config --global http.proxy %proxy_url%
    git config --global https.proxy %proxy_url%
    echo 已设置代理：%proxy_url%
)
echo.
pause
goto menu

:reconfig_remote
echo.
echo 重新配置远程仓库...
echo ==================
echo.
echo 当前远程仓库：
git remote -v
echo.
echo 1. 切换到HTTPS（推荐）
echo 2. 切换到SSH
echo 3. 返回主菜单
echo.
set /p remote_choice=请选择: 

if "%remote_choice%"=="1" (
    echo 设置HTTPS远程仓库...
    git remote set-url origin https://github.com/HaoZY123456789/AI-News-Agent.git
    echo 完成：已切换到HTTPS
) else if "%remote_choice%"=="2" (
    echo 设置SSH远程仓库...
    git remote set-url origin git@github.com:HaoZY123456789/AI-News-Agent.git
    echo 完成：已切换到SSH
)
echo.
pause
goto menu

:setup_ssh
echo.
echo 配置SSH连接...
echo ==============
echo.
echo 检查SSH密钥：
if exist "%USERPROFILE%\.ssh\id_rsa.pub" (
    echo 找到SSH密钥：
    type "%USERPROFILE%\.ssh\id_rsa.pub"
    echo.
    echo 请将上述公钥添加到GitHub SSH keys设置中
) else (
    echo 未找到SSH密钥，正在生成...
    ssh-keygen -t rsa -b 4096 -C "haozy123456789@example.com"
    echo.
    echo SSH密钥已生成，公钥内容：
    type "%USERPROFILE%\.ssh\id_rsa.pub"
    echo.
    echo 请将上述公钥添加到GitHub SSH keys设置中
)
echo.
echo 测试SSH连接：
ssh -T git@github.com
echo.
pause
goto menu

:test_connection
echo.
echo 测试Git连接...
echo ==============
echo.
echo 1. 测试拉取（fetch）
git fetch --dry-run
echo.
echo 2. 测试推送（push）
git push --dry-run
echo.
echo 3. 检查仓库状态
git status
echo.
pause
goto menu

:show_error_info
echo.
echo Git连接错误详细信息
echo ==================
echo.
echo 常见错误原因：
echo 1. 网络防火墙阻止HTTPS连接
echo 2. 公司代理设置问题
echo 3. GitHub服务器临时不可用
echo 4. SSL证书验证失败
echo 5. HTTP缓冲区太小
echo.
echo 解决方案优先级：
echo 1. 首选：修复HTTPS连接（选项2）
echo 2. 备选：配置代理设置（选项3）
echo 3. 高级：使用SSH连接（选项5）
echo.
echo 错误代码含义：
echo - Connection was reset：连接被重置
echo - SSL certificate problem：SSL证书问题
echo - Failed to connect：连接失败
echo - Timeout：连接超时
echo.
pause
goto menu

:exit
echo.
echo 快速解决方案总结：
echo ================
echo.
echo 最常用的解决方法：
echo 1. 运行"选项2：修复Git HTTPS连接问题"
echo 2. 如果仍失败，尝试"选项3：配置Git代理设置"
echo 3. 高级用户可使用"选项5：SSH连接"
echo.
echo 手动解决命令：
echo git config --global http.sslVerify false
echo git config --global http.postBuffer 524288000
echo git push
echo.
echo 感谢使用Git连接修复工具！
pause
exit