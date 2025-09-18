#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI资讯智能体测试脚本
用于测试各个模块的功能
"""

import os
import sys
import unittest
from datetime import datetime
import tempfile
import configparser

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestAINewsAgent(unittest.TestCase):
    """AI资讯智能体测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时配置文件
        self.temp_config = tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False)
        config_content = """
[email]
smtp_server = smtp.gmail.com
smtp_port = 587
sender_email = test@example.com
sender_password = test_password
receiver_email = test@example.com

[scraping]
update_interval_hours = 2
max_articles_per_send = 5

[sources]
test_source = https://example.com/rss

[database]
db_path = test_ai_news.db
"""
        self.temp_config.write(config_content)
        self.temp_config.close()
        self.config_file = self.temp_config.name
    
    def tearDown(self):
        """测试后清理"""
        # 删除临时文件
        if os.path.exists(self.config_file):
            os.unlink(self.config_file)
        # 尝试删除测试数据库文件，忽略权限错误
        try:
            if os.path.exists('test_ai_news.db'):
                os.unlink('test_ai_news.db')
        except PermissionError:
            pass  # 文件可能还在使用中，忽略错误
    
    def test_database_module(self):
        """测试数据库模块"""
        try:
            from database import NewsDatabase
            
            db = NewsDatabase(self.config_file)
            
            # 测试添加文章
            test_articles = [
                {
                    'title': '测试文章1',
                    'link': 'https://example.com/1',
                    'summary': '测试摘要1',
                    'source': 'test_source',
                    'published': datetime.now()
                },
                {
                    'title': '测试文章2',
                    'link': 'https://example.com/2',
                    'summary': '测试摘要2',
                    'source': 'test_source',
                    'published': datetime.now()
                }
            ]
            
            # 添加文章
            new_count = db.add_articles(test_articles)
            self.assertEqual(new_count, 2, "应该添加2篇新文章")
            
            # 测试去重
            unique_articles = db.get_duplicate_check_results(test_articles)
            self.assertEqual(len(unique_articles), 0, "去重后应该没有新文章")
            
            # 测试获取未发送文章
            unsent = db.get_unsent_articles()
            self.assertEqual(len(unsent), 2, "应该有2篇未发送文章")
            
            # 测试统计信息
            stats = db.get_statistics()
            self.assertEqual(stats['total_articles'], 2, "总文章数应该是2")
            self.assertEqual(stats['unsent_articles'], 2, "未发送文章数应该是2")
            
            print("✅ 数据库模块测试通过")
            
        except Exception as e:
            self.fail(f"数据库模块测试失败: {e}")
    
    def test_news_scraper_module(self):
        """测试新闻抓取模块"""
        try:
            from news_scraper import AINewsScraper
            
            scraper = AINewsScraper(self.config_file)
            
            # 测试关键词过滤
            test_articles = [
                {
                    'title': 'OpenAI releases new AI model',
                    'summary': 'Latest artificial intelligence breakthrough',
                    'published': datetime.now(),
                    'source': 'test'
                },
                {
                    'title': 'Regular tech news',
                    'summary': 'Nothing about technology here',
                    'published': datetime.now(),
                    'source': 'test'
                }
            ]
            
            filtered = scraper.filter_ai_keywords(test_articles)
            self.assertEqual(len(filtered), 1, "应该过滤出1篇AI相关文章")
            self.assertIn('AI', filtered[0]['title'], "过滤的文章应该包含AI关键词")
            
            print("✅ 新闻抓取模块测试通过")
            
        except Exception as e:
            self.fail(f"新闻抓取模块测试失败: {e}")
    
    def test_email_sender_module(self):
        """测试邮件发送模块（不实际发送）"""
        try:
            from email_sender import EmailSender
            
            sender = EmailSender(self.config_file)
            
            # 测试邮件内容生成
            test_articles = [
                {
                    'title': '测试文章',
                    'link': 'https://example.com',
                    'summary': '测试摘要',
                    'source': 'test_source',
                    'published': datetime.now()
                }
            ]
            
            html_content = sender.create_email_content(test_articles)
            
            # 检查HTML内容
            self.assertIn('测试文章', html_content, "HTML内容应该包含文章标题")
            self.assertIn('AI资讯日报', html_content, "HTML内容应该包含邮件标题")
            self.assertIn('https://example.com', html_content, "HTML内容应该包含文章链接")
            
            print("✅ 邮件发送模块测试通过")
            
        except Exception as e:
            self.fail(f"邮件发送模块测试失败: {e}")
    
    def test_scheduler_module(self):
        """测试调度器模块"""
        try:
            from scheduler import TaskScheduler
            
            scheduler = TaskScheduler(self.config_file)
            
            # 测试获取状态
            status = scheduler.get_status()
            
            self.assertIsInstance(status, dict, "状态应该是字典类型")
            self.assertIn('is_running', status, "状态应该包含运行状态")
            self.assertIn('update_interval', status, "状态应该包含更新间隔")
            
            print("✅ 调度器模块测试通过")
            
        except Exception as e:
            self.fail(f"调度器模块测试失败: {e}")
    
    def test_config_loading(self):
        """测试配置加载"""
        try:
            config = configparser.ConfigParser()
            config.read(self.config_file, encoding='utf-8')
            
            self.assertEqual(config.get('email', 'smtp_server'), 'smtp.gmail.com')
            self.assertEqual(config.get('scraping', 'update_interval_hours'), '2')
            self.assertEqual(config.get('database', 'db_path'), 'test_ai_news.db')
            
            print("✅ 配置加载测试通过")
            
        except Exception as e:
            self.fail(f"配置加载测试失败: {e}")

def run_integration_test():
    """运行集成测试"""
    print("\n🧪 运行AI资讯智能体集成测试")
    print("=" * 50)
    
    try:
        # 检查所有必需模块是否可以导入
        modules_to_test = [
            'news_scraper',
            'email_sender', 
            'database',
            'scheduler',
            'main'
        ]
        
        print("📦 检查模块导入...")
        for module_name in modules_to_test:
            try:
                __import__(module_name)
                print(f"✅ {module_name} 模块导入成功")
            except ImportError as e:
                print(f"❌ {module_name} 模块导入失败: {e}")
                return False
        
        print("\n🔧 运行单元测试...")
        
        # 运行单元测试
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(TestAINewsAgent)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        if result.wasSuccessful():
            print("\n🎉 所有测试通过！AI资讯智能体已准备就绪。")
            print("\n🚀 快速开始:")
            print("1. 运行配置向导: python config_wizard.py")
            print("2. 启动智能体: python main.py")
            return True
        else:
            print(f"\n❌ 测试失败: {len(result.failures)} 个失败, {len(result.errors)} 个错误")
            return False
            
    except Exception as e:
        print(f"❌ 集成测试过程出错: {e}")
        return False

def main():
    """主函数"""
    print("AI资讯智能体测试工具")
    print("=" * 30)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--unit':
        # 只运行单元测试
        unittest.main(argv=[''], exit=False)
    else:
        # 运行集成测试
        success = run_integration_test()
        if not success:
            sys.exit(1)

if __name__ == "__main__":
    main()