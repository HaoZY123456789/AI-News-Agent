#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI资讯智能体主程序
手动执行模式：支持单次抓取、测试邮件、查看统计等
"""

import argparse
import sys
import os
import logging
from pathlib import Path

# 添加项目路径到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scheduler import TaskScheduler
from email_sender import EmailSender
from database import NewsDatabase

class AINewsAgent:
    """AI资讯智能体主程序（手动模式）"""
    
    def __init__(self):
        self.scheduler = TaskScheduler()
        self.email_sender = EmailSender()
        self.database = NewsDatabase()
        
        # 设置日志
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
    
    def setup_logging(self):
        """设置日志配置"""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # 创建logs目录
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(log_dir / 'ai_news_agent.log', encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def run_once(self):
        """执行一次抓取任务"""
        self.logger.info("🔄 手动执行AI资讯抓取任务")
        try:
            self.scheduler.run_once()
            self.logger.info("✅ 任务执行完成")
            print("\n📧 如需查看收到的邮件，请检查您的邮箱")
            print("📊 如需查看统计信息，请运行: python main.py --stats")
        except Exception as e:
            self.logger.error(f"❌ 任务执行失败: {e}")
            sys.exit(1)
    
    def send_test_email(self):
        """发送测试邮件"""
        self.logger.info("📧 发送测试邮件")
        try:
            success = self.email_sender.send_test_email()
            if success:
                self.logger.info("✅ 测试邮件发送成功")
            else:
                self.logger.error("❌ 测试邮件发送失败")
                sys.exit(1)
        except Exception as e:
            self.logger.error(f"❌ 发送测试邮件时出错: {e}")
            sys.exit(1)
    
    def show_stats(self):
        """显示统计信息"""
        self.logger.info("📊 获取数据库统计信息")
        try:
            stats = self.database.get_statistics()
            
            print("\n🤖 AI资讯智能体 - 统计信息")
            print("=" * 50)
            print(f"📰 总文章数：{stats.get('total_articles', 0)}")
            print(f"📤 未发送文章：{stats.get('unsent_articles', 0)}")
            print(f"✅ 已发送文章：{stats.get('sent_articles', 0)}")
            print(f"⏰ 最后发送时间：{stats.get('last_send_time', '无')}")
            
            print(f"\n📊 各来源文章统计：")
            for source, count in stats.get('articles_by_source', {}).items():
                print(f"  • {source}: {count} 篇")
                
        except Exception as e:
            self.logger.error(f"❌ 获取统计信息失败: {e}")
            sys.exit(1)
    
    def cleanup_old_data(self):
        """清理旧数据"""
        self.logger.info("🧹 清理旧数据")
        try:
            self.database.cleanup_old_articles(days=30)
            self.logger.info("✅ 旧数据清理完成")
        except Exception as e:
            self.logger.error(f"❌ 清理旧数据失败: {e}")
            sys.exit(1)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='AI资讯智能体 - 手动抓取和推送AI相关资讯',
        epilog="""
使用示例:
  python main.py --once             # 执行一次抓取
  python main.py --test-email       # 发送测试邮件
  python main.py --stats            # 显示统计信息
  python main.py --cleanup          # 清理旧数据
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--once', action='store_true',
                       help='执行一次抓取任务后退出')
    parser.add_argument('--test-email', action='store_true',
                       help='发送测试邮件')
    parser.add_argument('--stats', action='store_true',
                       help='显示统计信息')
    parser.add_argument('--cleanup', action='store_true',
                       help='清理旧数据（30天前的已发送文章）')
    parser.add_argument('--version', action='version', version='AI资讯智能体 v1.1（手动模式）')
    
    args = parser.parse_args()
    
    # 如果没有指定参数，显示帮助和提示
    if not any(vars(args).values()):
        parser.print_help()
        print("\n💡 提示：这是手动执行模式，需要指定参数运行")
        print("   最常用：python main.py --once（执行一次抓取）")
        return
    
    # 创建智能体实例
    agent = AINewsAgent()
    
    # 根据参数执行对应功能
    if args.once:
        agent.run_once()
    elif args.test_email:
        agent.send_test_email()
    elif args.stats:
        agent.show_stats()
    elif args.cleanup:
        agent.cleanup_old_data()

if __name__ == "__main__":
    main()