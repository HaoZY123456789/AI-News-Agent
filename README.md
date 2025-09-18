# 🤖 AI资讯智能体 Android版

[![Android APK 构建](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/android-build.yml/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/android-build.yml)

一个智能的AI资讯抓取和推送应用，支持Android平台。

## ✨ 功能特色

- 🌐 **多源抓取** - 17个国内外权威AI资讯源
- 🤖 **智能分析** - AI关键词提取和文章总结
- 📧 **邮件推送** - 自动发送精选AI资讯到邮箱
- 📱 **Android原生** - 完整的移动端应用体验
- 🎨 **现代界面** - Material Design风格界面

## 📱 Android APK下载

APK文件通过GitHub Actions自动构建：

1. 访问 [Actions页面](../../actions)
2. 选择最新的构建
3. 下载 `ai-news-agent-apk` 文件
4. 在Android设备上安装

## 🚀 使用方法

### Android版本
1. 下载并安装APK
2. 首次运行配置邮箱信息
3. 点击"刷新"开始抓取AI资讯
4. 查看文章列表和AI分析

### 桌面版本
```bash
# 手动抓取一次
python main.py --once

# 查看统计信息
python main.py --stats

# 发送测试邮件
python main.py --test-email
```

## 🛠️ 技术栈

- **语言**: Python 3.11+
- **UI框架**: Kivy + KivyMD
- **数据库**: SQLite
- **构建工具**: Buildozer + GitHub Actions
- **支持平台**: Android 5.0+, Windows, Linux

## 📊 资讯源

### 国外源
- OpenAI Blog, DeepMind, TechCrunch AI
- arXiv AI/ML, MIT AI News
- VentureBeat AI, Wired AI, NVIDIA AI

### 国内源  
- 36氪, 机器之心, 雷锋网
- IT之家, 极客公园, 爱范儿

## 🔧 开发构建

### 本地开发
```bash
pip install -r requirements_android.txt
python main_android.py  # Android版本预览
python main.py --once   # 桌面版本
```

### APK构建
- **推荐**: 使用GitHub Actions自动构建
- **本地**: WSL2 + Ubuntu环境
- **Docker**: 使用提供的Dockerfile

## 📋 构建指南

详细的构建说明请查看：
- [GitHub Actions构建指南](GitHub_Actions构建指南.md)
- [Android构建指南](Android构建指南.md)

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

---

**让AI资讯触手可及！** 🚀📱

# 🤖 AI资讯智能体（手动模式）

手动抓取AI相关资讯并发送邮件通知的智能工具。

## ✨ 主要功能

- 🔍 **智能抓取**：从30+国内外权威AI资讯源自动抓取内容
- 🏷️ **关键词识别**：支持中英文AI关键词智能识别和过滤
- 🤖 **智能总结**：对每篇文章进行结构化总结，包含核心要点和影响分析
- 🔄 **手动执行**：需要时手动运行，简单可控
- 📧 **邮件推送**：手动发送格式化的AI资讯邮件
- 🗄️ **数据管理**：SQLite数据库存储，支持去重和历史管理

## 🛠️ 技术特性

### 改进后的智能总结功能
- ✅ **真正的内容分析**：不再是简单的模板回复
- ✅ **结构化输出**：包含文章概述、核心要点、影响分析
- ✅ **智能分类**：基于内容和关键词进行智能分类
- ✅ **多维度分析**：技术影响、市场影响、政策影响等

### 示例总结输出：
```
📰 文章标题：OpenAI推出新版ChatGPT-5模型，性能大幅提升

📝 内容概述：
OpenAI公司今日发布了最新的ChatGPT-5大语言模型，该模型在自然语言理解、代码生成...

🏷️ 关键主题：ChatGPT, OpenAI, 大语言模型

🎯 核心要点：
• 涉及大语言模型技术发展
• 可能包含技术升级或新版本发布

📊 影响分析：
可能对AI对话系统和自然语言处理领域产生积极影响

📱 来源：TechCrunch
```

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install requests beautifulsoup4 schedule feedparser
```

### 2. 配置邮箱
编辑 `config.ini`：
```ini
[email]
smtp_server = smtp.qq.com
smtp_port = 465
sender_email = your_email@qq.com
sender_password = your_auth_code  # QQ邮箱授权码
receiver_email = your_email@qq.com
```

### 3. 测试邮件功能
```bash
python main.py --test-email
```

### 4. 执行一次抓取
```bash
python main.py --once
```

### 5. 查看统计信息
```bash
python main.py --stats
```

## 📊 使用指令

```bash
# 执行一次抓取（最常用）
python main.py --once

# 发送测试邮件
python main.py --test-email

# 查看统计信息
python main.py --stats

# 清理旧数据
python main.py --cleanup

# 查看帮助
python main.py --help
```

## 📊 使用统计

查看统计信息：
```bash
python main.py --stats
```

输出示例：
```
🤖 AI资讯智能体 - 统计信息
==================================================
📰 总文章数：156
📤 未发送文章：12
✅ 已发送文章：144
⏰ 最后发送时间：2025-09-15 00:46:51

📊 各来源文章统计：
  • ithome: 45 篇
  • techcrunch_ai: 23 篇
  • kr36_ai: 18 篇
```

## 📁 项目结构

```
QoderProject/
├── main.py                 # 主程序入口
├── news_scraper.py         # 新闻抓取和智能总结
├── email_sender.py         # 邮件发送
├── database.py             # 数据库管理
├── scheduler.py            # 任务调度
├── config.ini              # 配置文件
├── 使用指南.md              # 详细使用说明
└── logs/                   # 日志目录
    └── ai_news_agent.log
```

## 🔧 配置说明

### 邮件配置
- QQ邮箱需要使用授权码，不是登录密码
- 支持其他SMTP邮箱服务

### 资讯源配置
包含30+国内外权威AI资讯源：
- **国外**：TechCrunch AI、The Verge、MIT News、OpenAI Blog等
- **国内**：36氪、IT之家、极客公园、雷锋网等

### 关键词库
支持中英文AI关键词：
- 技术类：人工智能、机器学习、深度学习、神经网络等
- 产品类：ChatGPT、GPT、大语言模型、智能体等
- 公司类：OpenAI、Google、百度、腾讯、阿里巴巴等

## 🐛 故障排除

### 邮件发送失败
1. 检查QQ邮箱是否开启SMTP服务
2. 确认使用授权码而非登录密码
3. 检查网络连接

### RSS源访问失败
- 部分国外源可能需要代理
- 程序会自动跳过失败的源

### 日志查看
```bash
tail -f logs/ai_news_agent.log
```

## 📝 更新日志

### v1.1.1 (2025-09-15)
- ✅ **简化为手动模式**：移除自动运行功能，专注手动执行
- ✅ **优化用户体验**：简化命令和使用流程
- ✅ **完善文档**：更新使用指南和README

### v1.1.0 (2025-09-15)
- ✅ **改进AI总结功能**：真正的内容分析，不再是模板回复
- ✅ **新增智能分析**：核心要点提取和影响分析
- ✅ **优化邮件显示**：结构化总结格式
- ✅ **修复SMTP问题**：解决QQ邮箱连接异常

### v1.0.0 (2025-09-14)
- 🎉 初始版本发布
- ✅ 基础抓取和邮件功能
- ✅ 中英文关键词识别
- ✅ SQLite数据库支持

## 📞 支持

如有问题或建议，请查看：
- `使用指南.md` - 详细使用说明
- `logs/ai_news_agent.log` - 运行日志
- 使用 `python main.py --help` 查看命令帮助

---

🎉 **现在您可以按需手动获取最新AI资讯了！**