# -*- coding: utf-8 -*-
"""
Created on Sun Sep 14 22:27:27 2025

@author: Administrator
"""

# 在您的IDE中运行这段代码
import sys
import os

# 添加项目路径并切换工作目录
sys.path.append('D:/QoderProject')
os.chdir('D:/QoderProject')

# 导入主程序
from main import AINewsAgent

# 创建智能体实例
print("🤖 创建AI资讯智能体...")
agent = AINewsAgent()

# 执行一次抓取任务
print("🔄 开始执行抓取任务...")
agent.run_once()
print("✅ 任务完成！")