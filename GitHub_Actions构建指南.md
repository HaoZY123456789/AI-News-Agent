# 🚀 GitHub Actions APK自动构建指南

## 📋 使用步骤

### 1. 📤 上传项目到GitHub

#### 方法一：使用GitHub Desktop（推荐新手）
1. 下载安装 [GitHub Desktop](https://desktop.github.com/)
2. 登录您的GitHub账户
3. 点击 "Add an Existing Repository from your Hard Drive"
4. 选择项目文件夹：`d:\QoderProject`
5. 发布到GitHub（选择仓库名称，如：`ai-news-agent`）

#### 方法二：使用Git命令行
```bash
# 在项目目录下执行
git init
git add .
git commit -m "Initial commit: AI资讯智能体 Android版本"
git branch -M main
git remote add origin https://github.com/你的用户名/ai-news-agent.git
git push -u origin main
```

### 2. 🏗️ 自动构建APK

一旦代码推送到GitHub，构建将自动开始：

1. **触发构建的情况：**
   - 推送代码到 `main` 或 `master` 分支
   - 修改了 `.py` 文件、`buildozer.spec` 或 `config.ini`
   - 手动触发构建

2. **构建过程：**
   ```
   📦 检出代码 → 🐍 设置Python → ☕ 设置Java → 🔧 安装依赖 → 📱 安装构建工具 → 🏗️ 构建APK → 📤 上传文件
   ```

3. **构建时间：** 通常需要 15-25 分钟

### 3. 📱 下载APK

构建完成后：

1. 进入GitHub仓库页面
2. 点击 "Actions" 标签
3. 选择最新的构建
4. 在 "Artifacts" 部分下载：
   - `ai-news-agent-apk` - APK安装文件
   - `build-report` - 构建报告

### 4. 📋 手动触发构建

如果需要手动重新构建：

1. 进入GitHub仓库的 "Actions" 页面
2. 选择 "AI资讯智能体 Android APK 构建" 工作流
3. 点击 "Run workflow" 按钮
4. 选择分支并点击 "Run workflow"

## 🔧 配置说明

### 📁 关键文件

- **`.github/workflows/android-build.yml`** - GitHub Actions工作流配置
- **`buildozer-github.spec`** - GitHub专用的Buildozer配置
- **`requirements_android.txt`** - Android构建依赖

### ⚙️ 构建配置

工作流自动配置了：
- ✅ Ubuntu 最新版本环境
- ✅ Python 3.11
- ✅ Java 17 (Temurin)
- ✅ Android SDK 33
- ✅ Android NDK 25b
- ✅ 自动接受SDK许可证
- ✅ 最新稳定版本的GitHub Actions

### 📱 APK规格

构建的APK特性：
- **应用名称：** AI资讯智能体
- **包名：** com.qoder.ainews
- **版本：** 1.0
- **支持架构：** ARM64-v8a, ARMv7a
- **最低Android版本：** 5.0 (API 21)
- **目标Android版本：** 13 (API 33)

## 🛠️ 故障排除

### 常见问题解决

#### 1. 构建失败
- 检查代码中是否有语法错误
- 确认所有依赖库都在 `requirements_android.txt` 中
- 查看构建日志中的具体错误信息

#### 2. APK无法安装
- 确保Android设备开启了"未知来源"安装权限
- 检查设备Android版本是否为5.0或以上
- 尝试重新下载APK文件

#### 3. 构建超时
- GitHub Actions有6小时的时间限制
- 通常APK构建在30分钟内完成
- 如果超时，请检查依赖配置

### 📊 查看构建日志

如果构建失败：
1. 进入 "Actions" 页面
2. 点击失败的构建
3. 展开各个步骤查看详细日志
4. 特别关注红色的错误信息

## 🎯 优势特点

### 🌟 GitHub Actions的优势

1. **完全免费** - 公开仓库免费使用
2. **自动化** - 代码推送后自动构建
3. **稳定环境** - Ubuntu云环境，依赖完整
4. **版本管理** - 每次构建都有记录
5. **多平台支持** - 可同时构建多个架构

### 🚀 适合场景

- ✅ 首次APK构建
- ✅ 定期发布更新
- ✅ 团队协作开发
- ✅ 版本控制需求
- ✅ 无本地Linux环境

## 📝 注意事项

### 🔒 隐私和安全

- 不要将敏感信息（如邮箱密码）直接写在代码中
- 使用GitHub Secrets存储敏感配置
- 可以选择私有仓库以保护代码

### 📄 许可证

- 建议添加适当的开源许可证
- 确保使用的所有库都符合许可要求

### 🔄 更新维护

- 定期更新依赖库版本
- 关注Android API版本更新
- 测试新版本的兼容性

---

## 🎉 开始使用

准备好了吗？按照上述步骤将您的项目上传到GitHub，几分钟后您就能获得第一个Android APK了！

**📱 您的AI资讯智能体即将在Android设备上运行！** 🚀