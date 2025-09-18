#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整流程测试脚本 - 测试文章总结功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from news_scraper import AINewsScraper
from database import NewsDatabase
from email_sender import EmailSender
import sqlite3

def test_complete_flow():
    """测试完整的文章处理流程"""
    print("🧪 测试AI资讯智能体完整流程")
    print("=" * 50)
    
    # 初始化组件
    scraper = AINewsScraper()
    db = NewsDatabase()
    email_sender = EmailSender()
    
    print("步骤1: 清理现有未发送文章以便重新测试...")
    try:
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()
            # 删除所有未发送的文章
            cursor.execute('DELETE FROM articles WHERE is_sent = 0')
            deleted_count = cursor.rowcount
            conn.commit()
            print(f"   清理了 {deleted_count} 篇未发送文章")
    except Exception as e:
        print(f"   清理失败: {e}")
    
    print("\n步骤2: 抓取AI资讯...")
    all_articles = scraper.get_ai_news()
    print(f"   原始文章数量: {len(all_articles)}")
    
    print("\n步骤3: 过滤AI相关文章...")
    filtered_articles = scraper.filter_ai_keywords(all_articles)
    print(f"   过滤后文章数量: {len(filtered_articles)}")
    
    print("\n步骤4: 对文章进行智能总结...")
    summarized_articles = scraper.summarize_articles_batch(filtered_articles)
    print(f"   完成总结的文章数量: {len(summarized_articles)}")
    
    # 显示前几篇文章的总结示例
    if summarized_articles:
        print("\n📄 总结示例:")
        for i, article in enumerate(summarized_articles[:2], 1):
            print(f"\n文章 {i}:")
            print(f"   标题: {article['title'][:50]}...")
            print(f"   关键词: {', '.join(article.get('detected_keywords', [])[:3])}")
            if article.get('ai_summary'):
                summary_lines = article['ai_summary'].split('\n')
                print(f"   总结: {summary_lines[0] if summary_lines else '无'}...")
    
    print("\n步骤5: 保存到数据库...")
    unique_articles = db.get_duplicate_check_results(summarized_articles)
    new_count = db.add_articles(unique_articles)
    print(f"   新增文章数量: {new_count}")
    
    print("\n步骤6: 检查数据库中的文章...")
    unsent_articles = db.get_unsent_articles(limit=3)
    print(f"   未发送文章数量: {len(unsent_articles)}")
    
    if unsent_articles:
        print("\n📰 数据库中的文章信息:")
        for i, article in enumerate(unsent_articles, 1):
            print(f"\n文章 {i}:")
            print(f"   标题: {article['title']}")
            print(f"   关键词: {', '.join(article.get('detected_keywords', []))}")
            print(f"   总结状态: {'已生成' if article.get('ai_summary') else '未生成'}")
            
            if article.get('ai_summary'):
                print(f"   总结预览: {article['ai_summary'][:100]}...")
    
    print("\n步骤7: 测试邮件发送...")
    if unsent_articles:
        try:
            success = email_sender.send_news_email(unsent_articles[:2])  # 只发送前2篇测试
            if success:
                print("   ✅ 邮件发送成功！")
                print("   请检查您的邮箱，确认文章总结是否正确显示")
            else:
                print("   ❌ 邮件发送失败")
        except Exception as e:
            print(f"   ❌ 邮件发送出错: {e}")
    else:
        print("   ⚠️  没有文章可发送")
    
    print("\n" + "=" * 50)
    print("🎉 完整流程测试完成！")
    print("请检查您的邮箱，确认收到的邮件中是否包含:")
    print("• 🏷️ 检测到的AI关键词")
    print("• 🤖 AI智能总结内容")

if __name__ == "__main__":
    test_complete_flow()