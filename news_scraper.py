import requests
import feedparser
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import time
import configparser

class AINewsScraper:
    """AI资讯抓取器"""
    
    def __init__(self, config_file: str = 'config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file, encoding='utf-8')
        
        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scraper.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # 请求头，模拟浏览器访问
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # RSS源配置
        self.rss_sources = dict(self.config.items('sources'))
        
    def fetch_rss_feed(self, url: str, source_name: str) -> List[Dict]:
        """抓取RSS源数据"""
        articles = []
        try:
            self.logger.info(f"正在抓取 {source_name}: {url}")
            
            # 设置超时和重试
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            # 解析RSS
            feed = feedparser.parse(response.content)
            
            for entry in feed.entries:
                # 解析发布时间
                published_time = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published_time = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published_time = datetime(*entry.updated_parsed[:6])
                else:
                    published_time = datetime.now()
                
                # 只获取最近10小时的文章
                if published_time and (datetime.now() - published_time).total_seconds() > 10 * 3600:
                    continue
                
                # 提取摘要，处理HTML标签
                summary = ""
                if hasattr(entry, 'summary'):
                    soup = BeautifulSoup(entry.summary, 'html.parser')
                    summary = soup.get_text().strip()[:300] + "..."
                
                article = {
                    'title': entry.title,
                    'link': entry.link,
                    'summary': summary,
                    'published': published_time,
                    'source': source_name,
                    'content_hash': hash(entry.title + entry.link)  # 用于去重
                }
                
                articles.append(article)
                
            self.logger.info(f"从 {source_name} 获取到 {len(articles)} 篇文章")
            
        except Exception as e:
            self.logger.error(f"抓取 {source_name} 时出错: {str(e)}")
            
        return articles
    
    def scrape_web_article(self, url: str) -> Optional[str]:
        """抓取网页文章内容（备用方法）"""
        try:
            response = requests.get(url, headers=self.headers, timeout=20)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 尝试找到文章内容
            content_selectors = [
                'article', '.article-content', '.post-content', 
                '.entry-content', '.content', 'main'
            ]
            
            content = ""
            for selector in content_selectors:
                element = soup.select_one(selector)
                if element:
                    content = element.get_text().strip()
                    break
            
            # 清理内容，限制长度
            if content:
                content = ' '.join(content.split())[:500] + "..."
                
            return content
            
        except Exception as e:
            self.logger.error(f"抓取网页内容失败 {url}: {str(e)}")
            return None
    
    def get_ai_news(self) -> List[Dict]:
        """获取所有AI资讯"""
        all_articles = []
        
        for source_name, url in self.rss_sources.items():
            articles = self.fetch_rss_feed(url, source_name)
            all_articles.extend(articles)
            
            # 添加延迟，避免请求过快
            time.sleep(2)
        
        # 按发布时间排序
        all_articles.sort(key=lambda x: x['published'], reverse=True)
        
        self.logger.info(f"总共获取到 {len(all_articles)} 篇AI资讯")
        return all_articles
    
    def filter_ai_keywords(self, articles: List[Dict]) -> List[Dict]:
        """根据AI关键词过滤文章（多层筛选，更精准）"""
        
        # 第一层：高优先级关键词（新工具、新模型发布相关）
        high_priority_keywords = [
            # 新AI工具/平台发布
            'released', 'launched', 'introduced', 'unveiled', 'announced', 'debuts',
            '发布', '推出', '上线', '发布会', '正式发布', '宣布', '首发', '开源',
            
            # 新大模型相关
            'new model', 'latest model', 'breakthrough model', 'next-generation',
            '新模型', '最新模型', '新一代', '突破性模型', '全新模型',
            
            # 版本更新
            'version', 'v2', 'v3', 'v4', '2.0', '3.0', '4.0', 'update', 'upgrade',
            '版本', '升级', '更新', 'beta', 'alpha',
            
            # 技术突破
            'breakthrough', 'milestone', 'achievement', 'innovation', 'revolutionary',
            '突破', '里程碑', '创新', '革命性', '颠覆性',
        ]
        
        # 第二层：核心AI技术关键词
        core_ai_keywords = [
            # 大模型相关
            'gpt', 'llm', 'large language model', 'transformer', 'chatgpt', 'claude', 
            'gemini', 'llama', 'bert', 'palm', 'deepseek', 'qwen', 'baichuan',
            '大语言模型', '大模型', '生成式AI', '对话模型',
            
            # AI工具平台
            'copilot', 'cursor', 'qoder', 'trae', 'midjourney', 'dalle', 'stable diffusion',
            'sora', 'runway', 'luma', 'pika', 'kling', '文心一言', '通义千问', 'kimi',
            
            # 技术公司/组织
            'openai', 'anthropic', 'google ai', 'deepmind', 'microsoft ai', 'meta ai',
            'nvidia', 'hugging face', '百度', '阿里巴巴', '腾讯', '字节跳动', '华为',
            '科大讯飞', '商汤', '旷视', '智谱AI', '月之暗面', '面壁智能',
            
            # AI应用领域
            'artificial intelligence', 'machine learning', 'deep learning', 'neural network',
            'computer vision', 'natural language processing', 'generative ai', 'multimodal',
            '人工智能', '机器学习', '深度学习', '神经网络', '计算机视觉', 
            '自然语言处理', '多模态', '智能体', 'agent',
        ]
        
        # 第三层：排除关键词（降低噪音）
        exclude_keywords = [
            'advertisement', 'promotion', 'marketing', 'sponsored', 'affiliate',
            '广告', '推广', '营销', '赞助', '联盟',
            'tutorial', 'how to', 'guide', 'tips', 'tricks',
            '教程', '如何', '指南', '技巧', '攻略',
        ]
        
        filtered_articles = []
        for article in articles:
            title = article['title']
            summary = article['summary']
            content = f"{title} {summary}"
            content_lower = content.lower()
            
            # 计算文章相关性分数
            relevance_score = 0
            detected_keywords = []
            
            # 检查高优先级关键词（权重3）
            for keyword in high_priority_keywords:
                if keyword.lower() in content_lower:
                    relevance_score += 3
                    detected_keywords.append(keyword)
            
            # 检查核心AI关键词（权重1）
            for keyword in core_ai_keywords:
                if keyword.lower() in content_lower:
                    relevance_score += 1
                    detected_keywords.append(keyword)
            
            # 检查排除关键词（负权重）
            for keyword in exclude_keywords:
                if keyword.lower() in content_lower:
                    relevance_score -= 2
            
            # 额外加分项：标题中包含关键词
            title_lower = title.lower()
            if any(keyword.lower() in title_lower for keyword in high_priority_keywords):
                relevance_score += 2
            
            # 筛选条件：相关性分数 >= 4 且包含至少一个核心关键词
            has_core_keyword = any(keyword.lower() in content_lower for keyword in core_ai_keywords)
            
            if relevance_score >= 4 and has_core_keyword:
                # 去重并限制关键词数量
                unique_keywords = list(dict.fromkeys(detected_keywords))  # 保持顺序去重
                article['detected_keywords'] = unique_keywords[:5]
                article['relevance_score'] = relevance_score
                filtered_articles.append(article)
        
        # 按相关性分数降序排序
        filtered_articles.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        self.logger.info(f"使用精准筛选策略，过滤后剩余 {len(filtered_articles)} 篇高质量AI文章")
        
        # 输出前几篇文章的得分用于调试
        for i, article in enumerate(filtered_articles[:3]):
            self.logger.info(f"文章{i+1}: 得分{article.get('relevance_score', 0)} - {article['title'][:50]}...")
            
        return filtered_articles
    
    def summarize_article(self, article: Dict) -> str:
        """对单篇文章进行精简智能总结"""
        try:
            title = article.get('title', '')
            summary = article.get('summary', '')
            source = article.get('source', '')
            keywords = article.get('detected_keywords', [])
            
            # 合并标题和摘要用于分析
            content = f"{title} {summary}"
            
            # 提取关键信息
            analysis_result = self._analyze_content_concise(content, keywords)
            
            # 生成精简的结构化总结
            summary_text = f"""
📰 {title}

🎯 核心亮点：{analysis_result['key_insight']}

📊 价值判断：{analysis_result['value_assessment']}

📱 来源：{source}
"""
            
            return summary_text
            
        except Exception as e:
            self.logger.error(f"文章总结失败: {str(e)}")
            return f"文章标题: {article.get('title', '')}。总结生成失败：{str(e)}"
    
    def _analyze_content_concise(self, content: str, keywords: List[str]) -> Dict[str, str]:
        """精简分析文章内容并提取关键信息"""
        content_lower = content.lower()
        
        # 核心亮点提取（一句话概括）
        key_insight = self._extract_key_insight(content, keywords)
        
        # 价值判断（简洁评估）
        value_assessment = self._assess_value(content, keywords)
        
        return {
            'key_insight': key_insight,
            'value_assessment': value_assessment
        }
    
    def _extract_key_insight(self, content: str, keywords: List[str]) -> str:
        """提取核心亮点（一句话总结）"""
        content_lower = content.lower()
        
        # 根据关键词类型生成精简亮点
        
        # 新模型/工具发布
        if any(kw in ['released', 'launched', 'unveiled', '发布', '推出', '上线'] for kw in keywords):
            if any(kw in ['gpt', 'llm', '大语言模型', '大模型'] for kw in keywords):
                return "新大语言模型正式发布，性能和能力有显著提升"
            elif any(kw in ['ai tool', 'platform', '平台', '工具'] for kw in keywords):
                return "新AI工具/平台发布，为用户提供更好的AI体验"
            else:
                return "重要AI产品或技术正式发布"
        
        # 技术突破
        elif any(kw in ['breakthrough', 'milestone', '突破', '里程碑', '创新'] for kw in keywords):
            if any(kw in ['performance', '性能', 'capability', '能力'] for kw in keywords):
                return "技术性能实现重大突破，超越现有水平"
            else:
                return "AI技术取得重要突破性进展"
        
        # 投资融资
        elif any(kw in ['investment', 'funding', '融资', '投资'] for kw in keywords):
            return "AI公司获得重要资本注入，促进技术发展"
        
        # 版本更新
        elif any(kw in ['version', 'update', 'upgrade', '版本', '升级', '更新'] for kw in keywords):
            return "产品版本重大更新，功能和性能进一步优化"
        
        # 合作伙伴
        elif any(kw in ['partnership', 'collaboration', '合作', '战略联盟'] for kw in keywords):
            return "AI领域重要合作达成，推动行业发展"
        
        # 市场竞争
        elif any(kw in ['competition', 'market', '竞争', '市场'] for kw in keywords):
            return "AI市场竞争格局发生变化，影响行业走向"
        
        # 政策监管
        elif any(kw in ['policy', 'regulation', '政策', '监管', '法规'] for kw in keywords):
            return "AI相关政策或监管出台，影响行业发展方向"
        
        # 默认情况
        else:
            return "AI领域值得关注的重要动态"
    
    def _assess_value(self, content: str, keywords: List[str]) -> str:
        """评估文章价值（简洁判断）"""
        content_lower = content.lower()
        
        # 高价值关键词
        high_value_indicators = [
            'breakthrough', 'revolutionary', 'milestone', 'first-ever', 'unprecedented',
            '突破', '革命性', '里程碑', '首次', '史上首次', '前所未有',
            'launched', 'released', 'unveiled', 'announced',
            '发布', '推出', '上线', '正式发布'
        ]
        
        # 中等价值关键词
        medium_value_indicators = [
            'funding', 'investment', 'partnership', 'collaboration',
            '融资', '投资', '合作', '战略联盟',
            'update', 'upgrade', 'improvement',
            '更新', '升级', '改进'
        ]
        
        # 低价值关键词
        low_value_indicators = [
            'analysis', 'report', 'study', 'survey', 'tutorial',
            '分析', '报告', '研究', '调查', '教程'
        ]
        
        # 计算价值分数
        value_score = 0
        
        for indicator in high_value_indicators:
            if indicator.lower() in content_lower:
                value_score += 3
                
        for indicator in medium_value_indicators:
            if indicator.lower() in content_lower:
                value_score += 2
                
        for indicator in low_value_indicators:
            if indicator.lower() in content_lower:
                value_score -= 1
        
        # 根据分数返回价值判断
        if value_score >= 6:
            return "🔥 高价值资讯，对行业影响重大"
        elif value_score >= 3:
            return "🟡 重要资讯，值得持续关注"
        elif value_score >= 0:
            return "🔵 一般资讯，了解即可"
        else:
            return "⚪ 参考信息，价值有限"
    
    def _generate_content_summary(self, content: str) -> str:
        """生成内容概述"""
        # 简化内容，去除HTML标签和多余空格
        import re
        clean_content = re.sub(r'<[^>]+>', '', content)
        clean_content = ' '.join(clean_content.split())
        
        # 截取前300个字符作为概述基础
        if len(clean_content) > 300:
            summary_base = clean_content[:300] + "..."
        else:
            summary_base = clean_content
            
        return summary_base
    
    def _extract_key_points(self, content: str, keywords: List[str]) -> str:
        """提取核心要点"""
        content_lower = content.lower()
        points = []
        
        # 根据不同类型的AI关键词提取要点
        if any(kw in ['ChatGPT', 'GPT', '大语言模型', 'LLM', '生成式AI'] for kw in keywords):
            if 'gpt' in content_lower or 'chatgpt' in content_lower:
                points.append("• 涉及大语言模型技术发展")
            if any(word in content_lower for word in ['升级', 'update', '更新', '发布']):
                points.append("• 可能包含技术升级或新版本发布")
                
        elif any(kw in ['机器学习', 'machine learning', 'ML', '深度学习'] for kw in keywords):
            if any(word in content_lower for word in ['算法', 'algorithm', '模型', 'model']):
                points.append("• 涉及机器学习算法或模型改进")
            if any(word in content_lower for word in ['训练', 'training', '数据', 'data']):
                points.append("• 可能讨论训练方法或数据处理技术")
                
        elif any(kw in ['自动驾驶', '智能驾驶', 'autonomous', '汽车'] for kw in keywords):
            if any(word in content_lower for word in ['测试', 'test', '路测', '试验']):
                points.append("• 可能涉及自动驾驶测试或试验")
            if any(word in content_lower for word in ['安全', 'safety', '事故', '法规']):
                points.append("• 关注自动驾驶安全性或法规问题")
                
        elif any(kw in ['机器人', 'robot', 'robotics'] for kw in keywords):
            if any(word in content_lower for word in ['服务', 'service', '应用', 'application']):
                points.append("• 涉及机器人服务应用")
            if any(word in content_lower for word in ['制造', 'manufacturing', '工业', 'industrial']):
                points.append("• 可能关注工业机器人发展")
                
        # 通用要点检测
        if any(word in content_lower for word in ['突破', 'breakthrough', '创新', 'innovation']):
            points.append("• 可能包含技术突破或创新")
        if any(word in content_lower for word in ['投资', 'investment', '融资', 'funding']):
            points.append("• 涉及投资或融资信息")
        if any(word in content_lower for word in ['竞争', 'competition', '市场', 'market']):
            points.append("• 涉及市场竞争态势")
        if any(word in content_lower for word in ['政策', 'policy', '监管', 'regulation']):
            points.append("• 可能涉及政策或监管动态")
            
        if not points:
            points.append("• 包含AI领域相关技术或市场信息")
            
        return '\n'.join(points[:4])  # 最多显示4个要点
    
    def _analyze_impact(self, content: str, keywords: List[str]) -> str:
        """分析潜在影响"""
        content_lower = content.lower()
        
        # 技术影响分析
        if any(kw in ['ChatGPT', 'GPT', '大语言模型'] for kw in keywords):
            if any(word in content_lower for word in ['能力', 'capability', '性能', 'performance']):
                return "可能对AI对话系统和自然语言处理领域产生积极影响"
            elif any(word in content_lower for word in ['风险', 'risk', '问题', 'problem']):
                return "需要关注大语言模型的潜在风险和伦理问题"
                
        elif any(kw in ['自动驾驶', '智能驾驶'] for kw in keywords):
            if any(word in content_lower for word in ['安全', 'safety']):
                return "对交通安全和智能交通系统发展具有重要意义"
            elif any(word in content_lower for word in ['商业化', 'commercial']):
                return "可能推动自动驾驶技术的商业化进程"
                
        elif any(kw in ['机器人'] for kw in keywords):
            if any(word in content_lower for word in ['服务', 'service']):
                return "可能改变服务行业的工作模式和效率"
            elif any(word in content_lower for word in ['制造', 'manufacturing']):
                return "对制造业自动化和效率提升有积极作用"
                
        # 通用影响分析
        if any(word in content_lower for word in ['突破', 'breakthrough']):
            return "技术突破可能推动整个AI行业的发展进步"
        elif any(word in content_lower for word in ['投资', 'investment', '融资']):
            return "资本动向可能影响AI产业的发展方向和速度"
        elif any(word in content_lower for word in ['政策', 'policy', '监管']):
            return "政策变化可能对AI行业发展产生规范和引导作用"
        else:
            return "为AI技术发展和应用提供有价值的参考信息"
    
    def summarize_articles_batch(self, articles: List[Dict]) -> List[Dict]:
        """批量对文章进行总结"""
        try:
            self.logger.info(f"开始对 {len(articles)} 篇文章进行总结...")
            
            for article in articles:
                article['ai_summary'] = self.summarize_article(article)
            
            self.logger.info(f"文章总结完成")
            return articles
            
        except Exception as e:
            self.logger.error(f"批量文章总结失败: {str(e)}")
            return articles

if __name__ == "__main__":
    # 测试抓取功能
    scraper = AINewsScraper()
    articles = scraper.get_ai_news()
    filtered_articles = scraper.filter_ai_keywords(articles)
    
    print(f"获取到 {len(filtered_articles)} 篇AI资讯")
    for i, article in enumerate(filtered_articles[:5]):
        print(f"\n{i+1}. {article['title']}")
        print(f"   来源: {article['source']}")
        print(f"   链接: {article['link']}")
        print(f"   时间: {article['published']}")
        print(f"   摘要: {article['summary'][:100]}...")