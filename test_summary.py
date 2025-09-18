#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文章总结功能的脚本
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import NewsDatabase

def test_article_summary():
    """测试文章总结功能"""
    print("🧪 测试文章总结功能")
    print("=" * 40)
    
    db = NewsDatabase()
    
    # 获取未发送的文章
    articles = db.get_unsent_articles(limit=3)
    
    if not articles:
        print("❌ 没有找到文章")
        return
    
    print(f"📰 找到 {len(articles)} 篇文章\n")
    
    for i, article in enumerate(articles, 1):
        print(f"📄 文章 {i}:")
        print(f"   标题: {article['title']}")
        print(f"   来源: {article['source']}")
        
        # 检查关键词
        if 'detected_keywords' in article and article['detected_keywords']:
            print(f"   🏷️  关键词: {', '.join(article['detected_keywords'][:3])}")
        else:
            print("   🏷️  关键词: 无")
        
        # 检查AI总结
        if 'ai_summary' in article and article['ai_summary']:
            summary_lines = article['ai_summary'].split('\n')
            print(f"   🤖 AI总结: 已生成 ({len(summary_lines)} 行)")
            # 显示总结的前几行
            for line in summary_lines[:3]:
                if line.strip():
                    print(f"      {line.strip()}")
        else:
            print("   🤖 AI总结: 无")
        
        print("-" * 50)

if __name__ == "__main__":
    test_article_summary()