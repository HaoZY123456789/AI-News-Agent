import schedule
import time
import logging
from datetime import datetime
import configparser
from typing import Callable
import threading
import signal
import sys

from news_scraper import AINewsScraper
from email_sender import EmailSender
from database import NewsDatabase

class TaskScheduler:
    """任务调度器"""
    
    def __init__(self, config_file: str = 'config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file, encoding='utf-8')
        
        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scheduler.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # 初始化组件
        self.scraper = AINewsScraper(config_file)
        self.email_sender = EmailSender(config_file)
        self.database = NewsDatabase(config_file)
        
        # 调度配置
        self.update_interval_hours = int(
            self.config.get('scraping', 'update_interval_hours', fallback='2')
        )
        self.max_articles_per_send = int(
            self.config.get('scraping', 'max_articles_per_send', fallback='10')
        )
        
        # 运行状态
        self.is_running = False
        self.scheduler_thread = None
        
        # 设置信号处理
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """处理停止信号"""
        self.logger.info(f"接收到停止信号 {signum}，正在关闭...")
        self.stop()
        sys.exit(0)
    
    def scrape_and_process_news(self):
        """抓取和处理新闻的核心任务"""
        try:
            self.logger.info("=" * 50)
            self.logger.info("开始执行新闻抓取任务")
            
            # 1. 抓取AI资讯
            self.logger.info("步骤1: 抓取AI资讯...")
            all_articles = self.scraper.get_ai_news()
            
            if not all_articles:
                self.logger.warning("没有抓取到任何文章")
                return
            
            # 2. 过滤AI相关内容
            self.logger.info("步骤2: 过滤AI相关内容...")
            filtered_articles = self.scraper.filter_ai_keywords(all_articles)
            
            if not filtered_articles:
                self.logger.warning("过滤后没有AI相关文章")
                return
            
            # 2.5. 对过滤后的文章进行总结
            self.logger.info("步骤2.5: 对AI文章进行智能总结...")
            summarized_articles = self.scraper.summarize_articles_batch(filtered_articles)
            
            # 3. 去重并添加到数据库
            self.logger.info("步骤3: 去重并保存到数据库...")
            unique_articles = self.database.get_duplicate_check_results(summarized_articles)
            new_articles_count = self.database.add_articles(unique_articles)
            
            # 4. 获取待发送的文章（包括之前未发送的）
            self.logger.info("步骤4: 准备发送邮件...")
            unsent_articles = self.database.get_unsent_articles(
                limit=self.max_articles_per_send
            )
            
            if not unsent_articles:
                self.logger.info("没有待发送的文章")
                if new_articles_count == 0:
                    self.logger.info("也没有新文章，任务完成")
                return
            
            # 5. 发送邮件
            self.logger.info(f"步骤5: 发送邮件，包含 {len(unsent_articles)} 篇文章（其中 {new_articles_count} 篇新文章）...")
            send_success = self.email_sender.send_news_email(unsent_articles)
            
            # 6. 更新发送状态
            if send_success:
                article_ids = [article['id'] for article in unsent_articles]
                self.database.mark_articles_as_sent(article_ids)
                self.database.log_send_result(len(unsent_articles), True)
                self.logger.info("任务执行成功！")
            else:
                self.database.log_send_result(len(unsent_articles), False, "邮件发送失败")
                self.logger.error("邮件发送失败")
            
            # 7. 清理旧数据
            self.logger.info("步骤6: 清理旧数据...")
            self.database.cleanup_old_articles(days=30)
            
            self.logger.info("新闻抓取任务完成")
            self.logger.info("=" * 50)
            
        except Exception as e:
            self.logger.error(f"执行新闻抓取任务时出错: {str(e)}")
            self.database.log_send_result(0, False, str(e))
    
    def send_daily_summary(self):
        """发送每日统计摘要"""
        try:
            self.logger.info("生成每日统计摘要...")
            stats = self.database.get_statistics()
            
            summary_text = f"""
📊 AI资讯智能体 - 每日统计报告

📈 数据统计：
• 总文章数：{stats.get('total_articles', 0)}
• 待发送：{stats.get('unsent_articles', 0)}
• 已发送：{stats.get('sent_articles', 0)}
• 最后发送：{stats.get('last_send_time', '无')}

📰 来源统计：
"""
            
            for source, count in stats.get('articles_by_source', {}).items():
                summary_text += f"• {source}: {count} 篇\n"
            
            # 这里可以选择发送统计邮件
            self.logger.info("每日统计摘要生成完成")
            
        except Exception as e:
            self.logger.error(f"生成每日统计摘要时出错: {str(e)}")
    
    def setup_schedule(self):
        """设置调度任务"""
        try:
            # 主要的新闻抓取任务
            schedule.every(self.update_interval_hours).hours.do(
                self.scrape_and_process_news
            )
            
            # 每日清理任务（凌晨3点执行）
            schedule.every().day.at("03:00").do(
                self.database.cleanup_old_articles, days=30
            )
            
            # 每周统计摘要（周一上午9点）
            schedule.every().monday.at("09:00").do(
                self.send_daily_summary
            )
            
            self.logger.info(f"调度任务设置完成:")
            self.logger.info(f"• 新闻抓取: 每 {self.update_interval_hours} 小时执行一次")
            self.logger.info(f"• 数据清理: 每天凌晨3点执行")
            self.logger.info(f"• 统计摘要: 每周一上午9点执行")
            
        except Exception as e:
            self.logger.error(f"设置调度任务失败: {str(e)}")
    
    def run_scheduler(self):
        """运行调度器的内部方法"""
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
            except Exception as e:
                self.logger.error(f"调度器运行出错: {str(e)}")
                time.sleep(60)
    
    def start(self):
        """启动调度器"""
        if self.is_running:
            self.logger.warning("调度器已在运行中")
            return
        
        try:
            self.logger.info("正在启动AI资讯智能体...")
            
            # 设置调度任务
            self.setup_schedule()
            
            # 启动时执行一次任务
            self.logger.info("执行启动时的首次抓取...")
            self.scrape_and_process_news()
            
            # 启动调度器线程
            self.is_running = True
            self.scheduler_thread = threading.Thread(target=self.run_scheduler)
            self.scheduler_thread.daemon = True
            self.scheduler_thread.start()
            
            self.logger.info("AI资讯智能体启动成功！")
            self.logger.info(f"下次执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 主线程保持运行
            try:
                while self.is_running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.stop()
                
        except Exception as e:
            self.logger.error(f"启动调度器失败: {str(e)}")
    
    def stop(self):
        """停止调度器"""
        if not self.is_running:
            return
        
        self.logger.info("正在停止AI资讯智能体...")
        self.is_running = False
        
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=5)
        
        # 清空调度任务
        schedule.clear()
        
        self.logger.info("AI资讯智能体已停止")
    
    def run_once(self):
        """手动执行一次抓取任务"""
        self.logger.info("手动执行抓取任务...")
        self.scrape_and_process_news()
    
    def get_next_run_time(self) -> str:
        """获取下次运行时间"""
        jobs = schedule.jobs
        if not jobs:
            return "无调度任务"
        
        next_run = min(job.next_run for job in jobs)
        return next_run.strftime('%Y-%m-%d %H:%M:%S')
    
    def get_status(self) -> dict:
        """获取调度器状态"""
        return {
            'is_running': self.is_running,
            'update_interval': self.update_interval_hours,
            'max_articles_per_send': self.max_articles_per_send,
            'next_run_time': self.get_next_run_time(),
            'scheduled_jobs': len(schedule.jobs)
        }

if __name__ == "__main__":
    # 创建调度器
    scheduler = TaskScheduler()
    
    # 显示状态
    print("AI资讯智能体调度器")
    print("=" * 30)
    status = scheduler.get_status()
    for key, value in status.items():
        print(f"{key}: {value}")
    
    print("\n选择操作:")
    print("1. 启动调度器（持续运行）")
    print("2. 执行一次抓取任务")
    print("3. 发送测试邮件")
    print("4. 退出")
    
    choice = input("\n请输入选择 (1-4): ").strip()
    
    if choice == "1":
        print("启动调度器...")
        scheduler.start()
    elif choice == "2":
        print("执行一次抓取任务...")
        scheduler.run_once()
    elif choice == "3":
        print("发送测试邮件...")
        email_sender = EmailSender()
        email_sender.send_test_email()
    elif choice == "4":
        print("退出程序")
    else:
        print("无效选择")