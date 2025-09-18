import smtplib
import logging
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import List, Dict
import configparser
from datetime import datetime

class EmailSender:
    """邮件发送器"""
    
    def __init__(self, config_file: str = 'config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file, encoding='utf-8')
        
        # 邮件配置
        self.smtp_server = self.config.get('email', 'smtp_server')
        self.smtp_port = int(self.config.get('email', 'smtp_port'))
        self.sender_email = self.config.get('email', 'sender_email')
        self.sender_password = self.config.get('email', 'sender_password')
        self.receiver_email = self.config.get('email', 'receiver_email')
        
        # 设置日志
        self.logger = logging.getLogger(__name__)
        
    def create_email_content(self, articles: List[Dict]) -> str:
        """创建邮件HTML内容"""
        
        # HTML模板
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ text-align: center; color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 20px; margin-bottom: 30px; }}
                .article {{ margin-bottom: 25px; padding: 15px; border-left: 4px solid #4CAF50; background-color: #f9f9f9; }}
                .article-title {{ font-size: 18px; font-weight: bold; color: #333; margin-bottom: 8px; }}
                .article-meta {{ color: #666; font-size: 12px; margin-bottom: 10px; }}
                .article-summary {{ color: #555; line-height: 1.6; margin-bottom: 10px; }}
                .article-keywords {{ background-color: #e8f5e8; padding: 5px 10px; margin: 10px 0; border-radius: 15px; font-size: 11px; }}
                .ai-summary {{ background-color: #f0f8ff; padding: 10px; margin: 10px 0; border-radius: 5px; border-left: 3px solid #2196F3; font-size: 13px; }}
                .article-link {{ color: #4CAF50; text-decoration: none; font-weight: bold; }}
                .article-link:hover {{ text-decoration: underline; }}
                .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #888; font-size: 12px; }}
                .stats {{ background-color: #e8f5e8; padding: 10px; border-radius: 5px; margin-bottom: 20px; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🤖 AI资讯日报</h1>
                    <p>您的专属AI新闻智能体为您精选</p>
                </div>
                
                <div class="stats">
                    <strong>📊 本期统计：共 {article_count} 篇文章 | 更新时间：{update_time}</strong>
                </div>
                
                {articles_html}
                
                <div class="footer">
                    <p>📧 此邮件由AI资讯智能体自动发送</p>
                    <p>🔄 下次更新时间：{next_update}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # 生成文章HTML
        articles_html = ""
        for i, article in enumerate(articles, 1):
            # 检测到的关键词
            keywords_html = ""
            if 'detected_keywords' in article and article['detected_keywords']:
                keywords = [kw for kw in article['detected_keywords'][:5] if kw.strip()]  # 最多显示5个，过滤空值
                if keywords:
                    keywords_html = f'<div class="article-keywords">🏷️ 关键词: {" • ".join(keywords)}</div>'
            
            # AI总结（精简版）
            ai_summary_html = ""
            if 'ai_summary' in article and article['ai_summary']:
                # 提取精简AI分析内容
                summary_lines = article['ai_summary'].split('\n')
                key_insight = ""
                value_assessment = ""
                
                for line in summary_lines:
                    line = line.strip()
                    if line.startswith('🎯 核心亮点：'):
                        key_insight = line.replace('🎯 核心亮点：', '').strip()
                    elif line.startswith('📊 价值判断：'):
                        value_assessment = line.replace('📊 价值判断：', '').strip()
                
                # 生成精简的AI分析显示
                if key_insight and value_assessment:
                    ai_summary_html = f'<div class="ai-summary">🤖 <strong>{key_insight}</strong> <span style="color: #666; font-size: 12px;">({value_assessment})</span></div>'
                elif key_insight:
                    ai_summary_html = f'<div class="ai-summary">🤖 {key_insight}</div>'
            
            article_html = f"""
            <div class="article">
                <div class="article-title">{i}. {article['title']}</div>
                <div class="article-meta">
                    📰 来源：{article['source']} | 
                    📅 发布时间：{article['published'].strftime('%Y-%m-%d %H:%M')}
                </div>
                {keywords_html}
                <div class="article-summary">{article['summary']}</div>
                {ai_summary_html}
                <div>
                    <a href="{article['link']}" class="article-link" target="_blank">
                        🔗 阅读全文 →
                    </a>
                </div>
            </div>
            """
            articles_html += article_html
        
        # 填充模板
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        next_update_hours = int(self.config.get('scraping', 'update_interval_hours', fallback='2'))
        next_update = f"{next_update_hours}小时后"
        
        html_content = html_template.format(
            article_count=len(articles),
            update_time=current_time,
            articles_html=articles_html,
            next_update=next_update
        )
        
        return html_content
    
    def send_news_email(self, articles: List[Dict]) -> bool:
        """发送AI资讯邮件"""
        try:
            if not articles:
                self.logger.info("没有新文章，跳过邮件发送")
                return True
            
            # 创建邮件对象
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f'🤖 AI资讯日报 - {datetime.now().strftime("%Y年%m月%d日")} ({len(articles)}篇)'
            msg['From'] = self.sender_email  # 使用简单格式，不包含显示名称
            msg['To'] = self.receiver_email
            
            # 创建HTML内容
            html_content = self.create_email_content(articles)
            
            # 创建纯文本内容（备用）
            text_content = f"""
AI资讯日报 - {datetime.now().strftime('%Y年%m月%d日')}

本期共有 {len(articles)} 篇AI相关文章：

"""
            for i, article in enumerate(articles, 1):
                text_content += f"""
{i}. {article['title']}
   来源：{article['source']}
   时间：{article['published'].strftime('%Y-%m-%d %H:%M')}
   摘要：{article['summary']}
   链接：{article['link']}

"""
            
            text_content += "\n此邮件由AI资讯智能体自动发送"
            
            # 添加文本和HTML部分
            text_part = MIMEText(text_content, 'plain', 'utf-8')
            html_part = MIMEText(html_content, 'html', 'utf-8')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            # 发送邮件
            self.logger.info(f"正在发送邮件到 {self.receiver_email}...")
            
            # 增加连接超时和重试机制
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # 根据端口选择连接方式
                    if self.smtp_port == 465:
                        # 使用SSL连接（QQ邮箱推荐）
                        server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, timeout=30)
                        try:
                            server.set_debuglevel(0)  # 设置为1可查看详细调试信息
                            server.login(self.sender_email, self.sender_password)
                            server.send_message(msg)
                        finally:
                            try:
                                server.quit()
                            except:
                                # 忽略QUIT命令的异常，因为邮件已经成功发送
                                pass
                    else:
                        # 使用TLS连接（Gmail等）
                        server = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=30)
                        try:
                            server.set_debuglevel(0)  # 设置为1可查看详细调试信息
                            server.starttls()  # 启用TLS加密
                            server.login(self.sender_email, self.sender_password)
                            server.send_message(msg)
                        finally:
                            try:
                                server.quit()
                            except:
                                # 忽略QUIT命令的异常，因为邮件已经成功发送
                                pass
                    
                    self.logger.info(f"邮件发送成功！发送了 {len(articles)} 篇文章")
                    return True
                    
                except smtplib.SMTPAuthenticationError as e:
                    self.logger.error(f"SMTP认证失败: {str(e)}")
                    self.logger.error("请检查邮箱地址和密码是否正确，QQ邮箱需要使用授权码而不是登录密码")
                    return False
                    
                except smtplib.SMTPConnectError as e:
                    self.logger.error(f"SMTP连接失败: {str(e)}")
                    if attempt < max_retries - 1:
                        self.logger.info(f"第 {attempt + 1} 次连接失败，{5} 秒后重试...")
                        time.sleep(5)
                        continue
                    else:
                        self.logger.error("所有连接尝试均失败")
                        return False
                        
                except Exception as e:
                    if attempt < max_retries - 1:
                        self.logger.warning(f"第 {attempt + 1} 次发送失败: {str(e)}，{3} 秒后重试...")
                        time.sleep(3)
                        continue
                    else:
                        self.logger.error(f"邮件发送失败: {str(e)}")
                        return False
            
            # 如果所有重试都失败，返回False
            return False
                        
        except Exception as e:
            self.logger.error(f"发送邮件时出现意外错误: {str(e)}")
            return False
    
    def send_test_email(self) -> bool:
        """发送测试邮件"""
        try:
            msg = MIMEMultipart()
            msg['Subject'] = '🧪 AI资讯智能体 - 测试邮件'
            msg['From'] = self.sender_email  # 使用简单格式，不包含显示名称
            msg['To'] = self.receiver_email
            
            test_content = """
            <html>
            <body>
                <h2>🎉 AI资讯智能体测试成功！</h2>
                <p>恭喜！您的AI资讯智能体已经配置成功，可以正常发送邮件了。</p>
                <p>接下来您将会定期收到精选的AI资讯。</p>
                <hr>
                <p><small>测试时间：{}</small></p>
            </body>
            </html>
            """.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            
            html_part = MIMEText(test_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # 增加连接超时和重试机制
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # 根据端口选择连接方式
                    if self.smtp_port == 465:
                        # 使用SSL连接（QQ邮箱推荐）
                        self.logger.info(f"使用SSL连接到 {self.smtp_server}:{self.smtp_port}")
                        server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, timeout=30)
                        try:
                            server.set_debuglevel(0)  # 启用调试信息
                            self.logger.info("正在进行认证...")
                            server.login(self.sender_email, self.sender_password)
                            self.logger.info("认证成功，正在发送邮件...")
                            server.send_message(msg)
                        finally:
                            try:
                                server.quit()
                            except:
                                # 忽略QUIT命令的异常，因为邮件已经成功发送
                                pass
                    else:
                        # 使用TLS连接（Gmail等）
                        self.logger.info(f"使用TLS连接到 {self.smtp_server}:{self.smtp_port}")
                        server = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=30)
                        try:
                            server.set_debuglevel(0)  # 启用调试信息
                            server.starttls()
                            self.logger.info("正在进行认证...")
                            server.login(self.sender_email, self.sender_password)
                            self.logger.info("认证成功，正在发送邮件...")
                            server.send_message(msg)
                        finally:
                            try:
                                server.quit()
                            except:
                                # 忽略QUIT命令的异常，因为邮件已经成功发送
                                pass
                    
                    self.logger.info("测试邮件发送成功！")
                    return True
                    
                except smtplib.SMTPAuthenticationError as e:
                    self.logger.error(f"SMTP认证失败: {str(e)}")
                    self.logger.error("请检查邮箱地址和密码是否正确，QQ邮箱需要使用授权码而不是登录密码")
                    return False
                    
                except Exception as e:
                    if attempt < max_retries - 1:
                        self.logger.warning(f"第 {attempt + 1} 次发送失败: {str(e)}，3 秒后重试...")
                        time.sleep(3)
                        continue
                    else:
                        self.logger.error(f"发送测试邮件失败: {str(e)}")
                        return False
            
            return False
            
        except Exception as e:
            self.logger.error(f"发送测试邮件失败: {str(e)}")
            return False

if __name__ == "__main__":
    # 测试邮件发送功能
    sender = EmailSender()
    
    # 创建测试文章数据
    test_articles = [
        {
            'title': 'OpenAI发布新一代GPT模型',
            'link': 'https://example.com/article1',
            'summary': '这是一个关于OpenAI最新GPT模型发布的测试文章摘要...',
            'published': datetime.now(),
            'source': 'TechCrunch'
        },
        {
            'title': '谷歌AI在医疗诊断领域取得突破',
            'link': 'https://example.com/article2', 
            'summary': '谷歌的人工智能系统在医疗图像诊断方面展现出超越人类专家的准确性...',
            'published': datetime.now(),
            'source': 'MIT News'
        }
    ]
    
    print("发送测试邮件...")
    sender.send_test_email()
    
    print("发送测试新闻邮件...")
    sender.send_news_email(test_articles)