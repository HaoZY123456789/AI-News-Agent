#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试改进后的AI总结功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from news_scraper import AINewsScraper

def test_improved_summary():
    """测试改进后的总结功能"""
    print("🧪 测试改进后的AI总结功能")
    print("=" * 50)
    
    scraper = AINewsScraper()
    
    # 创建测试文章数据
    test_articles = [
        {
            'title': 'OpenAI推出新版ChatGPT-5模型，性能大幅提升',
            'summary': 'OpenAI公司今日发布了最新的ChatGPT-5大语言模型，该模型在自然语言理解、代码生成和多模态处理方面都有显著提升。新模型采用了最新的Transformer架构，训练数据量比前一代增加了50%，在多项基准测试中表现优异。专家认为这将对AI行业产生重大影响，推动人工智能技术在更多场景下的应用。',
            'source': 'TechCrunch',
            'detected_keywords': ['ChatGPT', 'OpenAI', '大语言模型', 'AI', '人工智能']
        },
        {
            'title': '特斯拉自动驾驶系统通过新安全测试，获批在欧洲上路',
            'summary': '特斯拉的Full Self-Driving (FSD)自动驾驶系统近日通过了欧盟严格的安全测试，获得在欧洲道路上进行商业化运营的许可。该系统使用了先进的计算机视觉和深度学习算法，能够在复杂路况下做出准确判断。这一突破标志着自动驾驶技术在全球范围内的商业化进程又迈进了一大步。',
            'source': 'The Verge', 
            'detected_keywords': ['自动驾驶', '特斯拉', '深度学习', 'AI', '计算机视觉']
        },
        {
            'title': '中国AI芯片公司获得5亿美元融资，专注机器人应用',
            'summary': '国内知名AI芯片设计公司今日宣布完成5亿美元B轮融资，本轮融资将主要用于机器人专用AI芯片的研发和产业化。该公司表示，其最新研发的神经网络处理器在机器人运动控制和环境感知方面具有突出优势，已与多家机器人制造商达成合作协议。业内分析师认为，这将加速中国在智能机器人领域的技术突破。',
            'source': '36氪',
            'detected_keywords': ['AI芯片', '机器人', '融资', '神经网络', '人工智能']
        }
    ]
    
    print(f"📄 测试 {len(test_articles)} 篇文章的智能总结:")
    
    for i, article in enumerate(test_articles, 1):
        print(f"\n{'='*60}")
        print(f"测试文章 {i}: {article['title'][:40]}...")
        print('='*60)
        
        # 生成总结
        summary = scraper.summarize_article(article)
        print(summary)
        print()

if __name__ == "__main__":
    test_improved_summary()