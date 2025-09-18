#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI资讯智能体 - Android版本修复版（解决中文字体问题）
"""

import os
# 设置环境变量确保中文显示
os.environ['KIVY_WINDOW'] = 'sdl2'
os.environ['KIVY_TEXT'] = 'pil'

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.text import LabelBase
import threading
import sys
from datetime import datetime

# 导入核心模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scheduler import TaskScheduler
from email_sender import EmailSender
from database import NewsDatabase

class ArticleCard(BoxLayout):
    """文章卡片组件 - 修复版"""
    
    def __init__(self, article_data, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(200)
        self.padding = dp(10)
        self.spacing = dp(5)
        
        # 文章标题 - 修复中文显示
        title_text = article_data.get('title', '无标题')
        title_label = Label(
            text=title_text,
            font_size='14sp',
            halign='left',
            valign='top',
            size_hint_y=None,
            height=dp(60),
            text_size=(dp(350), dp(60)),
            markup=False
        )
        self.add_widget(title_label)
        
        # 来源和时间 - 简化显示
        source_text = f"来源: {article_data.get('source', '未知')}"
        time_text = f"时间: {article_data.get('published_at', '未知时间')}"
        
        source_label = Label(
            text=source_text,
            size_hint_y=None,
            height=dp(25),
            font_size='12sp',
            color=[0.5, 0.5, 0.5, 1],
            text_size=(dp(350), dp(25))
        )
        self.add_widget(source_label)
        
        time_label = Label(
            text=time_text,
            size_hint_y=None,
            height=dp(25),
            font_size='12sp',
            color=[0.5, 0.5, 0.5, 1],
            text_size=(dp(350), dp(25))
        )
        self.add_widget(time_label)
        
        # AI总结 - 简化显示
        if article_data.get('ai_summary'):
            summary_text = f"AI分析: {article_data['ai_summary']}"
            summary_label = Label(
                text=summary_text,
                font_size='13sp',
                halign='left',
                valign='top',
                size_hint_y=None,
                height=dp(50),
                color=[0.2, 0.5, 0.8, 1],
                text_size=(dp(350), dp(50))
            )
            self.add_widget(summary_label)
        
        # 关键词 - 简化显示
        if article_data.get('detected_keywords'):
            keywords_text = f"关键词: {article_data['detected_keywords']}"
            keywords_label = Label(
                text=keywords_text,
                size_hint_y=None,
                height=dp(30),
                font_size='11sp',
                color=[0.1, 0.7, 0.1, 1],
                text_size=(dp(350), dp(30))
            )
            self.add_widget(keywords_label)


class SettingsPopup(Popup):
    """设置弹窗 - 修复版"""
    
    def __init__(self, main_app, **kwargs):
        super().__init__(**kwargs)
        self.main_app = main_app
        self.title = '应用设置'
        self.size_hint = (0.9, 0.8)
        
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))
        
        # 邮件设置标题
        email_title = Label(
            text='邮件配置', 
            size_hint_y=None, 
            height=dp(40), 
            font_size='16sp'
        )
        content.add_widget(email_title)
        
        # 邮件配置网格
        email_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(120))
        
        email_layout.add_widget(Label(text='发送邮箱:', size_hint_x=0.3))
        self.sender_email = TextInput(text='1004274796@qq.com', multiline=False, size_hint_x=0.7)
        email_layout.add_widget(self.sender_email)
        
        email_layout.add_widget(Label(text='授权码:', size_hint_x=0.3))
        self.sender_password = TextInput(text='bfbwimtwngqybbbj', password=True, multiline=False, size_hint_x=0.7)
        email_layout.add_widget(self.sender_password)
        
        email_layout.add_widget(Label(text='接收邮箱:', size_hint_x=0.3))
        self.receiver_email = TextInput(text='1004274796@qq.com', multiline=False, size_hint_x=0.7)
        email_layout.add_widget(self.receiver_email)
        
        content.add_widget(email_layout)
        
        # 抓取设置标题
        scrape_title = Label(
            text='抓取设置', 
            size_hint_y=None, 
            height=dp(40), 
            font_size='16sp'
        )
        content.add_widget(scrape_title)
        
        # 抓取配置网格
        scrape_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(80))
        
        scrape_layout.add_widget(Label(text='更新间隔(小时):', size_hint_x=0.5))
        self.update_interval = TextInput(text='1', multiline=False, size_hint_x=0.5)
        scrape_layout.add_widget(self.update_interval)
        
        scrape_layout.add_widget(Label(text='每次最大文章数:', size_hint_x=0.5))
        self.max_articles = TextInput(text='30', multiline=False, size_hint_x=0.5)
        scrape_layout.add_widget(self.max_articles)
        
        content.add_widget(scrape_layout)
        
        # 自动抓取开关
        auto_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        auto_layout.add_widget(Label(text='启用自动抓取:', size_hint_x=0.7))
        self.auto_scraping = Switch(active=False, size_hint_x=0.3)
        auto_layout.add_widget(self.auto_scraping)
        content.add_widget(auto_layout)
        
        # 按钮
        button_layout = BoxLayout(orientation='horizontal', spacing=dp(20), size_hint_y=None, height=dp(50))
        
        save_btn = Button(text='保存设置', size_hint_x=0.5)
        save_btn.bind(on_press=self.save_settings)  # type: ignore
        button_layout.add_widget(save_btn)
        
        cancel_btn = Button(text='取消', size_hint_x=0.5)
        cancel_btn.bind(on_press=self.dismiss)  # type: ignore
        button_layout.add_widget(cancel_btn)
        
        content.add_widget(button_layout)
        self.content = content
    
    def save_settings(self, instance):
        """保存设置"""
        try:
            self.main_app.show_message('设置保存成功！')
            self.dismiss()
        except Exception as e:
            self.main_app.show_message(f'保存设置失败: {str(e)}')


class AINewsApp(App):
    """AI资讯智能体主应用 - 修复版"""
    
    def build(self):
        self.title = 'AI资讯智能体'
        
        # 初始化核心组件
        self.scheduler = TaskScheduler()
        self.email_sender = EmailSender()
        self.database = NewsDatabase()
        
        # 主布局
        main_layout = BoxLayout(orientation='vertical')
        
        # 顶部工具栏
        toolbar = BoxLayout(
            orientation='horizontal', 
            size_hint_y=None, 
            height=dp(60),
            padding=dp(10),
            spacing=dp(10)
        )
        
        # 标题
        title_label = Label(
            text='AI资讯智能体',
            font_size='18sp',
            size_hint_x=0.5,
            halign='left'
        )
        toolbar.add_widget(title_label)
        
        # 工具按钮
        refresh_btn = Button(
            text='刷新',
            size_hint_x=0.2,
            size_hint_y=None,
            height=dp(40)
        )
        refresh_btn.bind(on_press=self.manual_scrape)  # type: ignore
        toolbar.add_widget(refresh_btn)
        
        settings_btn = Button(
            text='设置',
            size_hint_x=0.2,
            size_hint_y=None,
            height=dp(40)
        )
        settings_btn.bind(on_press=self.show_settings)  # type: ignore
        toolbar.add_widget(settings_btn)
        
        main_layout.add_widget(toolbar)
        
        # 状态栏
        self.status_bar = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            padding=dp(10)
        )
        
        self.status_label = Label(
            text='准备就绪',
            font_size='14sp',
            size_hint_x=0.7
        )
        self.status_bar.add_widget(self.status_label)
        
        # 进度条
        self.progress_bar = ProgressBar(
            max=100,
            value=0,
            size_hint_x=0.3
        )
        self.status_bar.add_widget(self.progress_bar)
        
        main_layout.add_widget(self.status_bar)
        
        # 文章列表
        self.create_article_list()
        main_layout.add_widget(self.article_scroll)
        
        # 底部按钮栏
        bottom_bar = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            padding=dp(10),
            spacing=dp(10)
        )
        
        test_email_btn = Button(text='测试邮件')
        test_email_btn.bind(on_press=self.test_email)  # type: ignore
        bottom_bar.add_widget(test_email_btn)
        
        stats_btn = Button(text='统计')
        stats_btn.bind(on_press=self.show_stats)  # type: ignore
        bottom_bar.add_widget(stats_btn)
        
        cleanup_btn = Button(text='清理')
        cleanup_btn.bind(on_press=self.cleanup_data)  # type: ignore
        bottom_bar.add_widget(cleanup_btn)
        
        main_layout.add_widget(bottom_bar)
        
        # 定时更新UI
        Clock.schedule_interval(self.update_ui, 5.0)
        
        return main_layout
    
    def create_article_list(self):
        """创建文章列表"""
        self.article_scroll = ScrollView()
        self.article_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(10),
            size_hint_y=None
        )
        self.article_layout.bind(minimum_height=self.article_layout.setter('height'))  # type: ignore
        self.article_scroll.add_widget(self.article_layout)
        
        # 加载初始文章
        self.load_articles()
    
    def load_articles(self):
        """加载文章数据"""
        try:
            # 清空现有文章
            self.article_layout.clear_widgets()
            
            # 从数据库获取最新文章
            articles = self.database.get_recent_articles(limit=20)
            
            if not articles:
                no_articles_label = Label(
                    text='暂无文章数据\\n点击"刷新"开始抓取',
                    halign='center',
                    font_size='16sp',
                    size_hint_y=None,
                    height=dp(100)
                )
                self.article_layout.add_widget(no_articles_label)
                return
            
            # 创建文章卡片
            for article in articles:
                card = ArticleCard(article)
                self.article_layout.add_widget(card)
                
            self.status_label.text = f'已加载 {len(articles)} 篇文章'
            
        except Exception as e:
            error_label = Label(
                text=f'加载文章失败: {str(e)}',
                halign='center',
                color=[1, 0, 0, 1],
                size_hint_y=None,
                height=dp(60)
            )
            self.article_layout.add_widget(error_label)
    
    def manual_scrape(self, instance):
        """手动抓取"""
        self.status_label.text = '正在抓取AI资讯...'
        self.progress_bar.value = 0
        
        # 在后台线程执行抓取
        threading.Thread(target=self._do_scrape, daemon=True).start()
    
    def _do_scrape(self):
        """执行抓取任务"""
        try:
            # 模拟进度更新
            Clock.schedule_once(lambda dt: setattr(self.progress_bar, 'value', 25), 0.5)
            
            # 执行抓取
            self.scheduler.run_once()
            
            Clock.schedule_once(lambda dt: setattr(self.progress_bar, 'value', 100), 1.0)
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', '抓取完成'), 1.0)
            
            # 重新加载文章列表
            Clock.schedule_once(lambda dt: self.load_articles(), 1.5)
            
        except Exception as e:
            Clock.schedule_once(
                lambda dt: setattr(self.status_label, 'text', f'抓取失败: {str(e)}'),
                0
            )
    
    def test_email(self, instance):
        """测试邮件发送"""
        self.status_label.text = '正在发送测试邮件...'
        threading.Thread(target=self._do_test_email, daemon=True).start()
    
    def _do_test_email(self):
        """执行邮件测试"""
        try:
            success = self.email_sender.send_test_email()
            if success:
                Clock.schedule_once(
                    lambda dt: setattr(self.status_label, 'text', '测试邮件发送成功'),
                    0
                )
            else:
                Clock.schedule_once(
                    lambda dt: setattr(self.status_label, 'text', '测试邮件发送失败'),
                    0
                )
        except Exception as e:
            Clock.schedule_once(
                lambda dt: setattr(self.status_label, 'text', f'邮件测试错误: {str(e)}'),
                0
            )
    
    def show_stats(self, instance):
        """显示统计信息"""
        try:
            stats = self.database.get_statistics()
            
            stats_text = f"""数据库统计信息

总文章数: {stats.get('total_articles', 0)}
未发送: {stats.get('unsent_articles', 0)}
已发送: {stats.get('sent_articles', 0)}
最后发送: {stats.get('last_send_time', '无')}

各来源统计:
"""
            
            for source, count in stats.get('articles_by_source', {}).items():
                stats_text += f"{source}: {count} 篇\\n"
            
            popup = Popup(
                title='统计信息',
                content=Label(text=stats_text, halign='left', valign='top'),
                size_hint=(0.8, 0.6)
            )
            popup.open()
            
        except Exception as e:
            self.show_message(f'获取统计信息失败: {str(e)}')
    
    def cleanup_data(self, instance):
        """清理旧数据"""
        try:
            self.database.cleanup_old_articles(days=30)
            self.show_message('旧数据清理完成')
            self.load_articles()  # 重新加载文章列表
        except Exception as e:
            self.show_message(f'清理数据失败: {str(e)}')
    
    def show_settings(self, instance):
        """显示设置页面"""
        settings_popup = SettingsPopup(self)
        settings_popup.open()
    
    def show_message(self, message):
        """显示消息弹窗"""
        popup = Popup(
            title='提示',
            content=Label(text=message, halign='center'),
            size_hint=(0.6, 0.3)
        )
        popup.open()
    
    def update_ui(self, dt):
        """定时更新UI"""
        # 这里可以添加定时更新逻辑，比如检查新文章
        pass


if __name__ == '__main__':
    AINewsApp().run()