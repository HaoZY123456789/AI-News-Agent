#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试关键词和AI总结功能
"""

import sys
sys.path.append('.')

from news_scraper import AINewsScraper
from email_sender import EmailSender
from database import NewsDatabase
from datetime import datetime

def test_keywords_and_summary():
    """测试关键词检测和AI总结功能"""
    
    # 创建测试文章数据
    test_articles = [
        {
            'title': 'DeepSeek推出新一代大语言模型，性能超越GPT-4',
            'link': 'https://example.com/article1',
            'summary': 'DeepSeek公司今日发布了最新的大语言模型DeepSeek-V3，该模型在多项评测中表现出色，在代码生成、推理能力等方面超越了OpenAI的GPT-4模型。新模型采用了先进的Transformer架构和创新的训练技术，参数规模达到1750亿，支持多模态输入输出。',
            'published': datetime.now(),
            'source': 'TechCrunch',
            'content_hash': hash('test1')
        },
        {
            'title': '腾讯AI实验室发布智能体框架Qoder，助力编程效率提升',
            'link': 'https://example.com/article2',
            'summary': '腾讯AI实验室宣布开源智能体开发框架Qoder，该框架专为软件开发场景设计，集成了代码生成、调试、测试等多项功能。Qoder基于大语言模型技术，能够理解自然语言需求并自动生成高质量代码，显著提升开发效率。',
            'published': datetime.now(),
            'source': '36氪',
            'content_hash': hash('test2')
        },
        {
            'title': 'Trae AI平台获得千万美元融资，专注企业级AI解决方案',
            'link': 'https://example.com/article3',
            'summary': 'AI初创公司Trae今日宣布完成千万美元A轮融资，本轮融资由知名风投机构领投。Trae专注于为企业提供定制化的人工智能解决方案，其平台集成了机器学习、自然语言处理和计算机视觉等多项技术，已服务超过100家企业客户。',
            'published': datetime.now(),
            'source': 'VentureBeat',
            'content_hash': hash('test3')
        }
    ]
    
    print("🧪 开始测试关键词和AI总结功能...")
    print("=" * 50)
    
    # 初始化抓取器
    scraper = AINewsScraper()
    
    # 1. 测试关键词过滤
    print("\n📋 步骤1：测试关键词过滤...")
    filtered_articles = scraper.filter_ai_keywords(test_articles)
    print(f"原始文章数量：{len(test_articles)}")
    print(f"过滤后文章数量：{len(filtered_articles)}")
    
    for i, article in enumerate(filtered_articles, 1):
        print(f"\n文章 {i}：{article['title']}")
        print(f"检测到的关键词：{article.get('detected_keywords', [])}")
    
    # 2. 测试AI总结
    print("\n📝 步骤2：测试AI总结生成...")
    summarized_articles = scraper.summarize_articles_batch(filtered_articles)
    
    for i, article in enumerate(summarized_articles, 1):
        print(f"\n文章 {i} AI总结：")
        print("-" * 30)
        print(article.get('ai_summary', '无总结'))
    
    # 3. 测试邮件模板
    print("\n📧 步骤3：测试邮件模板...")
    email_sender = EmailSender()
    html_content = email_sender.create_email_content(summarized_articles)
    
    # 将HTML内容保存到文件，方便查看
    with open('test_email_preview.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("邮件HTML预览已保存到：test_email_preview.html")
    
    # 4. 测试数据库存储（简化版本）
    print("\n💾 步骤4：测试数据库存储...")
    db = NewsDatabase()
    
    # 直接使用批量添加方法
    added_count = db.add_articles(summarized_articles)
    print(f"成功添加 {added_count} 篇文章到数据库")
    
    # 验证数据库中的数据
    unsent_articles = db.get_unsent_articles()
    print(f"数据库中待发送文章数量：{len(unsent_articles)}")
    
    if unsent_articles:
        print("\n数据库中第一篇文章的关键词和总结：")
        first_article = unsent_articles[0]
        print(f"关键词：{first_article.get('detected_keywords', '')}")
        print(f"AI总结长度：{len(first_article.get('ai_summary', ''))}")
        print(f"AI总结前100字符：{first_article.get('ai_summary', '')[:100]}...")
    
    print("\n✅ 测试完成！")
    print("\n📋 测试结果总结：")
    print(f"- 关键词过滤：{'✅ 正常' if len(filtered_articles) > 0 else '❌ 异常'}")
    print(f"- AI总结生成：{'✅ 正常' if all('ai_summary' in article for article in summarized_articles) else '❌ 异常'}")
    print(f"- 数据库存储：{'✅ 正常' if added_count > 0 else '❌ 异常'}")
    print(f"- 邮件模板：{'✅ 正常' if len(html_content) > 1000 else '❌ 异常'}")

if __name__ == "__main__":
    test_keywords_and_summary()