import sqlite3
import logging
from typing import List, Dict, Set
from datetime import datetime, timedelta
import configparser
import hashlib

class NewsDatabase:
    """新闻数据库管理器"""
    
    def __init__(self, config_file: str = 'config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file, encoding='utf-8')
        
        self.db_path = self.config.get('database', 'db_path', fallback='ai_news.db')
        self.logger = logging.getLogger(__name__)
        
        # 初始化数据库
        self.init_database()
    
    def init_database(self):
        """初始化数据库表"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 创建文章表
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS articles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        link TEXT NOT NULL UNIQUE,
                        summary TEXT,
                        source TEXT,
                        published_date DATETIME,
                        scraped_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        content_hash TEXT UNIQUE,
                        is_sent INTEGER DEFAULT 0,
                        sent_date DATETIME,
                        detected_keywords TEXT,
                        ai_summary TEXT
                    )
                ''')
                
                # 添加新字段（如果表已存在）
                try:
                    cursor.execute('ALTER TABLE articles ADD COLUMN detected_keywords TEXT')
                    cursor.execute('ALTER TABLE articles ADD COLUMN ai_summary TEXT')
                except sqlite3.OperationalError:
                    # 字段已存在，忽略错误
                    pass
                
                # 创建发送记录表
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS send_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        send_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        article_count INTEGER,
                        success INTEGER,
                        error_message TEXT
                    )
                ''')
                
                # 创建索引
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_content_hash ON articles(content_hash)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_published_date ON articles(published_date)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_is_sent ON articles(is_sent)')
                
                conn.commit()
                self.logger.info("数据库初始化完成")
                
        except Exception as e:
            self.logger.error(f"数据库初始化失败: {str(e)}")
    
    def generate_content_hash(self, title: str, link: str) -> str:
        """生成内容哈希值用于去重"""
        content = f"{title}{link}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def add_articles(self, articles: List[Dict]) -> int:
        """批量添加文章，返回新增文章数量"""
        new_articles_count = 0
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for article in articles:
                    try:
                        # 生成内容哈希
                        content_hash = self.generate_content_hash(
                            article['title'], 
                            article['link']
                        )
                        
                        # 检查是否已存在
                        cursor.execute(
                            'SELECT id FROM articles WHERE content_hash = ?',
                            (content_hash,)
                        )
                        
                        if cursor.fetchone() is None:
                            # 提取关键词和总结
                            detected_keywords = ''
                            ai_summary = ''
                            
                            if 'detected_keywords' in article:
                                detected_keywords = ','.join(article['detected_keywords']) if article['detected_keywords'] else ''
                            
                            if 'ai_summary' in article:
                                ai_summary = article['ai_summary'] or ''
                            
                            # 插入新文章
                            cursor.execute('''
                                INSERT INTO articles 
                                (title, link, summary, source, published_date, content_hash, detected_keywords, ai_summary)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (
                                article['title'],
                                article['link'], 
                                article['summary'],
                                article['source'],
                                article['published'],
                                content_hash,
                                detected_keywords,
                                ai_summary
                            ))
                            new_articles_count += 1
                            
                    except sqlite3.IntegrityError:
                        # 重复文章，跳过
                        continue
                    except Exception as e:
                        self.logger.error(f"添加文章失败: {str(e)}")
                        continue
                
                conn.commit()
                self.logger.info(f"成功添加 {new_articles_count} 篇新文章")
                
        except Exception as e:
            self.logger.error(f"批量添加文章失败: {str(e)}")
        
        return new_articles_count
    
    def get_unsent_articles(self, limit: int | None = None) -> List[Dict]:
        """获取未发送的文章"""
        articles = []
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = '''
                    SELECT id, title, link, summary, source, published_date, content_hash, detected_keywords, ai_summary
                    FROM articles 
                    WHERE is_sent = 0
                    ORDER BY published_date DESC
                '''
                
                if limit:
                    query += f' LIMIT {limit}'
                
                cursor.execute(query)
                rows = cursor.fetchall()
                
                for row in rows:
                    # 解析关键词
                    detected_keywords = []
                    if row[7]:  # detected_keywords 字段
                        detected_keywords = row[7].split(',')
                    
                    articles.append({
                        'id': row[0],
                        'title': row[1],
                        'link': row[2],
                        'summary': row[3],
                        'source': row[4],
                        'published': datetime.fromisoformat(row[5]) if row[5] else None,
                        'content_hash': row[6],
                        'detected_keywords': detected_keywords,
                        'ai_summary': row[8] or ''  # ai_summary 字段
                    })
                    
        except Exception as e:
            self.logger.error(f"获取未发送文章失败: {str(e)}")
        
        return articles
    
    def mark_articles_as_sent(self, article_ids: List[int]) -> bool:
        """标记文章为已发送"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                placeholders = ','.join(['?'] * len(article_ids))
                cursor.execute(f'''
                    UPDATE articles 
                    SET is_sent = 1, sent_date = CURRENT_TIMESTAMP 
                    WHERE id IN ({placeholders})
                ''', article_ids)
                
                conn.commit()
                self.logger.info(f"标记 {len(article_ids)} 篇文章为已发送")
                return True
                
        except Exception as e:
            self.logger.error(f"标记文章为已发送失败: {str(e)}")
            return False
    
    def log_send_result(self, article_count: int, success: bool, error_message: str | None = None):
        """记录发送结果"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO send_logs (article_count, success, error_message)
                    VALUES (?, ?, ?)
                ''', (article_count, 1 if success else 0, error_message))
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"记录发送日志失败: {str(e)}")
    
    def cleanup_old_articles(self, days: int = 30):
        """清理旧文章数据"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 删除旧的已发送文章
                cursor.execute('''
                    DELETE FROM articles 
                    WHERE is_sent = 1 AND sent_date < ?
                ''', (cutoff_date.isoformat(),))
                
                deleted_count = cursor.rowcount
                conn.commit()
                
                self.logger.info(f"清理了 {deleted_count} 篇旧文章")
                
        except Exception as e:
            self.logger.error(f"清理旧文章失败: {str(e)}")
    
    def get_recent_articles(self, limit: int = 20) -> List[Dict]:
        """获取最近的文章（包括已发送和未发送）"""
        articles = []
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = '''
                    SELECT id, title, link, summary, source, published_date, 
                           scraped_date, is_sent, detected_keywords, ai_summary
                    FROM articles 
                    ORDER BY scraped_date DESC
                    LIMIT ?
                '''
                
                cursor.execute(query, (limit,))
                rows = cursor.fetchall()
                
                for row in rows:
                    # 解析关键词
                    detected_keywords = []
                    if row[8]:  # detected_keywords 字段
                        detected_keywords = row[8].split(',')
                    
                    # 格式化发布时间
                    published_at = '未知时间'
                    if row[5]:  # published_date
                        try:
                            pub_date = datetime.fromisoformat(row[5])
                            published_at = pub_date.strftime('%Y-%m-%d %H:%M')
                        except:
                            published_at = '未知时间'
                    
                    articles.append({
                        'id': row[0],
                        'title': row[1],
                        'link': row[2],
                        'summary': row[3],
                        'source': row[4],
                        'published_at': published_at,
                        'scraped_date': row[6],
                        'is_sent': bool(row[7]),
                        'detected_keywords': ', '.join(detected_keywords) if detected_keywords else '',
                        'ai_summary': row[9] or ''
                    })
                    
        except Exception as e:
            self.logger.error(f"获取最近文章失败: {str(e)}")
        
        return articles
    
    def get_statistics(self) -> Dict:
        """获取数据库统计信息"""
        stats = {}
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 总文章数
                cursor.execute('SELECT COUNT(*) FROM articles')
                stats['total_articles'] = cursor.fetchone()[0]
                
                # 未发送文章数
                cursor.execute('SELECT COUNT(*) FROM articles WHERE is_sent = 0')
                stats['unsent_articles'] = cursor.fetchone()[0]
                
                # 已发送文章数
                cursor.execute('SELECT COUNT(*) FROM articles WHERE is_sent = 1')
                stats['sent_articles'] = cursor.fetchone()[0]
                
                # 最近一次发送时间
                cursor.execute('SELECT MAX(send_date) FROM send_logs WHERE success = 1')
                last_send = cursor.fetchone()[0]
                stats['last_send_time'] = last_send
                
                # 各来源文章数
                cursor.execute('''
                    SELECT source, COUNT(*) 
                    FROM articles 
                    GROUP BY source 
                    ORDER BY COUNT(*) DESC
                ''')
                stats['articles_by_source'] = dict(cursor.fetchall())
                
        except Exception as e:
            self.logger.error(f"获取统计信息失败: {str(e)}")
        
        return stats
    
    def get_duplicate_check_results(self, articles: List[Dict]) -> List[Dict]:
        """检查文章重复并返回去重后的结果"""
        unique_articles = []
        existing_hashes = set()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 获取已存在的哈希值
                cursor.execute('SELECT content_hash FROM articles')
                existing_hashes = set(row[0] for row in cursor.fetchall())
                
            # 过滤重复文章
            for article in articles:
                content_hash = self.generate_content_hash(
                    article['title'], 
                    article['link']
                )
                
                if content_hash not in existing_hashes:
                    unique_articles.append(article)
                    existing_hashes.add(content_hash)  # 防止本批次内重复
                    
            self.logger.info(f"去重后剩余 {len(unique_articles)} 篇文章")
            
        except Exception as e:
            self.logger.error(f"去重检查失败: {str(e)}")
            return articles  # 失败时返回原列表
        
        return unique_articles

if __name__ == "__main__":
    # 测试数据库功能
    db = NewsDatabase()
    
    # 测试数据
    test_articles = [
        {
            'title': '测试文章1',
            'link': 'https://example.com/1',
            'summary': '这是测试文章1的摘要',
            'source': 'test_source',
            'published': datetime.now()
        },
        {
            'title': '测试文章2',
            'link': 'https://example.com/2',
            'summary': '这是测试文章2的摘要', 
            'source': 'test_source',
            'published': datetime.now()
        }
    ]
    
    # 测试添加文章
    print("测试添加文章...")
    new_count = db.add_articles(test_articles)
    print(f"新添加了 {new_count} 篇文章")
    
    # 测试获取未发送文章
    print("\n测试获取未发送文章...")
    unsent = db.get_unsent_articles(limit=5)
    print(f"未发送文章数量: {len(unsent)}")
    
    # 测试统计信息
    print("\n数据库统计信息:")
    stats = db.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # 测试去重
    print("\n测试去重功能...")
    unique_articles = db.get_duplicate_check_results(test_articles)
    print(f"去重后文章数量: {len(unique_articles)}")