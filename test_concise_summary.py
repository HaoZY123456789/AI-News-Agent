#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试精简AI总结功能
"""

import sys
sys.path.append('.')

from news_scraper import AINewsScraper
from email_sender import EmailSender
from datetime import datetime

def test_concise_summary():
    """测试精简AI总结功能"""
    
    # 创建测试文章数据
    test_articles = [
        {
            'title': 'OpenAI Launches GPT-5: Revolutionary Breakthrough in AI Reasoning',
            'link': 'https://example.com/article1',
            'summary': 'OpenAI today announced the release of GPT-5, featuring breakthrough capabilities in reasoning and multimodal understanding. The new model represents a significant milestone in artificial intelligence development.',
            'published': datetime.now(),
            'source': 'TechCrunch',
            'content_hash': hash('test1'),
            'detected_keywords': ['announced', 'released', 'breakthrough', 'new model', 'gpt', 'openai']
        },
        {
            'title': '阿里巴巴通义千问3.0获得重大融资，估值达500亿美元',
            'link': 'https://example.com/article2',
            'summary': '阿里巴巴旗下的通义千问大语言模型获得新一轮投资，本轮融资金额达到数十亿美元，公司估值达到500亿美元，标志着国产AI技术的重要里程碑。',
            'published': datetime.now(),
            'source': '36氪',
            'content_hash': hash('test2'),
            'detected_keywords': ['融资', 'investment', '通义千问', '大语言模型', '阿里巴巴']
        },
        {
            'title': 'Meta AI Improves Code Generation Capabilities with Update 2.1',
            'link': 'https://example.com/article3',
            'summary': 'Meta has released an update to its AI coding assistant, featuring improved code generation and debugging capabilities. The update includes better support for multiple programming languages.',
            'published': datetime.now(),
            'source': 'VentureBeat',
            'content_hash': hash('test3'),
            'detected_keywords': ['update', 'improved', 'code generation', 'meta', 'ai']
        },
        {
            'title': 'AI Research Report: Market Trends and Investment Analysis',
            'link': 'https://example.com/article4',
            'summary': 'A comprehensive analysis of the artificial intelligence market covering current trends, investment patterns, and future predictions for the AI industry.',
            'published': datetime.now(),
            'source': 'Research Institute',
            'content_hash': hash('test4'),
            'detected_keywords': ['report', 'analysis', 'market', 'ai', 'investment']
        }
    ]
    
    print("🧪 测试精简AI总结功能")
    print("=" * 60)
    
    # 初始化抓取器
    scraper = AINewsScraper()
    
    print(f"\n📝 对比新旧总结格式：")
    
    for i, article in enumerate(test_articles, 1):
        print(f"\n{'='*50}")
        print(f"📰 文章 {i}: {article['title'][:50]}...")
        print(f"🏷️ 关键词: {', '.join(article['detected_keywords'][:3])}")
        
        # 生成精简总结
        ai_summary = scraper.summarize_article(article)
        article['ai_summary'] = ai_summary
        
        print(f"\n🎯 精简AI分析：")
        print(ai_summary)
    
    # 测试邮件模板效果
    print(f"\n📧 测试邮件模板效果...")
    email_sender = EmailSender()
    html_content = email_sender.create_email_content(test_articles)
    
    # 保存HTML预览
    with open('test_concise_email_preview.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ 邮件HTML预览已保存到：test_concise_email_preview.html")
    
    # 分析改进效果
    print(f"\n📊 改进效果分析：")
    
    # 统计总结长度
    total_length = 0
    for article in test_articles:
        summary_length = len(article.get('ai_summary', ''))
        total_length += summary_length
        print(f"- {article['title'][:30]}... | 总结长度: {summary_length} 字符")
    
    avg_length = total_length / len(test_articles)
    print(f"\n平均总结长度：{avg_length:.0f} 字符")
    
    # 检查精简度
    if avg_length < 200:
        print("✅ 总结长度合适，精简有效")
    elif avg_length < 400:
        print("⚠️ 总结长度适中，可进一步精简")
    else:
        print("❌ 总结仍然过长，需要进一步优化")
    
    # 验证核心信息提取
    print(f"\n💡 核心信息提取验证：")
    for article in test_articles:
        summary = article.get('ai_summary', '')
        has_key_insight = '🎯 核心亮点：' in summary
        has_value_assessment = '📊 价值判断：' in summary
        
        status = "✅" if has_key_insight and has_value_assessment else "❌"
        print(f"{status} {article['title'][:30]}... | 包含核心亮点: {has_key_insight}, 价值判断: {has_value_assessment}")

if __name__ == "__main__":
    test_concise_summary()