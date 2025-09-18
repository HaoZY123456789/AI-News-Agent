@echo off
cd /d "%~dp0"
echo 🤖 AI资讯智能体 - 开始抓取
echo ================================
echo.
echo 📡 正在执行AI资讯抓取任务...
python main.py --once
echo.
echo ✅ 抓取任务完成
pause