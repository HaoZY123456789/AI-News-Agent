#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试精准筛选功能
"""

import sys
sys.path.append('.')

from news_scraper import AINewsScraper
from datetime import datetime

def test_precise_filtering():
    """测试新的精准筛选功能"""
    
    # 创建测试文章数据，包含不同类型的文章
    test_articles = [
        # 高质量AI工具发布文章
        {
            'title': 'OpenAI Launches GPT-5: Revolutionary Breakthrough in AI Reasoning',
            'link': 'https://example.com/article1',
            'summary': 'OpenAI today announced the release of GPT-5, featuring breakthrough capabilities in reasoning and multimodal understanding. The new model represents a significant milestone in artificial intelligence development.',
            'published': datetime.now(),
            'source': 'TechCrunch',
            'content_hash': hash('test1')
        },
        {
            'title': '字节跳动发布全新大模型豆包3.0，超越GPT-4性能表现',
            'link': 'https://example.com/article2', 
            'summary': '字节跳动正式发布豆包3.0大语言模型，在代码生成、数学推理等多个领域均有突破性进展，标志着国产AI技术新的里程碑。新版本采用全新架构设计，参数规模达到千亿级别。',
            'published': datetime.now(),
            'source': '36氪',
            'content_hash': hash('test2')
        },
        {
            'title': 'Anthropic Unveils Claude 4: Next-Generation AI Assistant with Enhanced Safety',
            'link': 'https://example.com/article3',
            'summary': 'Anthropic introduces Claude 4, the latest version of their AI assistant with revolutionary safety features and improved performance. The new model includes advanced reasoning capabilities and better alignment.',
            'published': datetime.now(),
            'source': 'VentureBeat',
            'content_hash': hash('test3')
        },
        # 中等质量文章
        {
            'title': 'AI Market Analysis: Trends and Predictions for 2024',
            'link': 'https://example.com/article4',
            'summary': 'A comprehensive analysis of the artificial intelligence market, covering investment trends, major players, and future predictions for the AI industry in 2024.',
            'published': datetime.now(),
            'source': 'Forbes',
            'content_hash': hash('test4')
        },
        {
            'title': '腾讯AI研究院：人工智能在医疗领域的应用现状',
            'link': 'https://example.com/article5',
            'summary': '腾讯AI研究院发布报告，详细分析了人工智能技术在医疗诊断、药物研发等领域的最新应用情况和发展趋势。',
            'published': datetime.now(),
            'source': '雷锋网',
            'content_hash': hash('test5')
        },
        # 低质量文章（应该被过滤）
        {
            'title': 'How to Use ChatGPT: Complete Tutorial for Beginners',
            'link': 'https://example.com/article6',
            'summary': 'Learn how to use ChatGPT effectively with this comprehensive tutorial. Tips and tricks for getting the best results from AI chatbots.',
            'published': datetime.now(),
            'source': 'Medium',
            'content_hash': hash('test6')
        },
        {
            'title': 'AI投资指南：如何选择人工智能股票',
            'link': 'https://example.com/article7',
            'summary': '为投资者提供AI股票投资攻略，包括如何分析人工智能公司的投资价值，以及相关的投资技巧和注意事项。',
            'published': datetime.now(),
            'source': '投资界',
            'content_hash': hash('test7')
        },
        # 噪音文章（包含AI但不相关）
        {
            'title': 'AI-Powered Marketing Promotion: Boost Your Sales',
            'link': 'https://example.com/article8',
            'summary': 'Discover how artificial intelligence can revolutionize your marketing campaigns. This sponsored content shows you the best AI marketing tools.',
            'published': datetime.now(),
            'source': 'Marketing Blog',
            'content_hash': hash('test8')
        }
    ]
    
    print("🧪 测试精准筛选功能")
    print("=" * 60)
    
    # 初始化抓取器
    scraper = AINewsScraper()
    
    print(f"\n📊 原始文章数量：{len(test_articles)}")
    print("\n原始文章列表：")
    for i, article in enumerate(test_articles, 1):
        print(f"{i}. {article['title']}")
    
    # 使用新的精准筛选
    print(f"\n🎯 使用精准筛选策略...")
    filtered_articles = scraper.filter_ai_keywords(test_articles)
    
    print(f"\n✅ 筛选结果：")
    print(f"筛选后文章数量：{len(filtered_articles)}")
    
    if filtered_articles:
        print(f"\n📋 筛选出的高质量文章：")
        for i, article in enumerate(filtered_articles, 1):
            score = article.get('relevance_score', 0)
            keywords = article.get('detected_keywords', [])
            print(f"\n{i}. 【评分：{score}】{article['title']}")
            print(f"   检测到的关键词：{', '.join(keywords[:3])}...")
            print(f"   来源：{article['source']}")
    else:
        print("没有文章通过精准筛选")
    
    # 分析筛选效果
    print(f"\n📈 筛选效果分析：")
    total_articles = len(test_articles)
    filtered_count = len(filtered_articles)
    filter_rate = (filtered_count / total_articles) * 100 if total_articles > 0 else 0
    
    print(f"- 筛选率：{filter_rate:.1f}% ({filtered_count}/{total_articles})")
    
    # 检查高质量文章是否被正确识别
    high_quality_titles = [
        'OpenAI Launches GPT-5',
        '字节跳动发布全新大模型豆包3.0',
        'Anthropic Unveils Claude 4'
    ]
    
    detected_high_quality = 0
    for article in filtered_articles:
        for hq_title in high_quality_titles:
            if hq_title in article['title']:
                detected_high_quality += 1
                break
    
    print(f"- 高质量文章识别率：{detected_high_quality}/{len(high_quality_titles)} ({(detected_high_quality/len(high_quality_titles)*100):.1f}%)")
    
    # 检查噪音文章是否被过滤
    noise_titles = ['How to Use ChatGPT', 'AI投资指南', 'AI-Powered Marketing Promotion']
    detected_noise = 0
    for article in filtered_articles:
        for noise_title in noise_titles:
            if noise_title in article['title']:
                detected_noise += 1
                break
    
    print(f"- 噪音过滤效果：{len(noise_titles)-detected_noise}/{len(noise_titles)} ({((len(noise_titles)-detected_noise)/len(noise_titles)*100):.1f}%)")
    
    # 显示推荐调整
    print(f"\n💡 建议：")
    if filter_rate > 70:
        print("- 筛选过于宽松，建议提高阈值")
    elif filter_rate < 30:
        print("- 筛选过于严格，建议适当降低阈值") 
    else:
        print("- 筛选策略适中，效果良好")
        
    if detected_high_quality == len(high_quality_titles):
        print("- 高质量文章识别完美 ✅")
    else:
        print("- 需要优化高质量文章识别规则")
        
    if detected_noise == 0:
        print("- 噪音过滤效果良好 ✅")
    else:
        print("- 需要加强噪音文章过滤")

if __name__ == "__main__":
    test_precise_filtering()