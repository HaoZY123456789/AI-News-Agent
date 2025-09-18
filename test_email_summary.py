#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的邮件测试脚本
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import NewsDatabase
from email_sender import EmailSender

def test_email_with_summary():
    """测试包含总结功能的邮件发送"""
    print("📧 测试包含文章总结的邮件发送")
    print("=" * 40)
    
    db = NewsDatabase()
    email_sender = EmailSender()
    
    # 获取有总结的文章
    articles = db.get_unsent_articles(limit=2)
    
    if not articles:
        print("❌ 没有找到文章")
        return
    
    print(f"📰 找到 {len(articles)} 篇文章")
    
    for i, article in enumerate(articles, 1):
        print(f"\n📄 文章 {i}:")
        print(f"   标题: {article['title'][:60]}...")
        print(f"   关键词: {', '.join(article.get('detected_keywords', [])[:3])}")
        print(f"   总结: {'✅ 已生成' if article.get('ai_summary') else '❌ 未生成'}")
    
    print(f"\n📧 正在发送包含 {len(articles)} 篇文章的邮件...")
    
    try:
        # 尝试发送邮件
        success = email_sender.send_news_email(articles)
        
        if success:
            print("✅ 邮件发送成功！")
            print("📬 请检查您的邮箱，确认是否收到包含以下内容的邮件：")
            print("   • 🏷️ AI关键词标签")
            print("   • 🤖 智能总结内容")
            print("   • 📊 文章分类分析")
            
            # 标记为已发送
            article_ids = [article['id'] for article in articles]
            db.mark_articles_as_sent(article_ids)
            print("✅ 文章已标记为已发送")
            
        else:
            print("❌ 邮件发送失败")
            
    except Exception as e:
        print(f"❌ 发送过程中出错: {e}")

if __name__ == "__main__":
    test_email_with_summary()