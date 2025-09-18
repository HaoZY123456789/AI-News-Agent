#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移动端配置管理器
专门处理Android平台的配置和存储
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any
from kivy.utils import platform
from kivy.storage.jsonstore import JsonStore

class MobileConfigManager:
    """移动端配置管理器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config_store = None
        self.default_config = {
            'email': {
                'smtp_server': 'smtp.qq.com',
                'smtp_port': 465,
                'sender_email': '1004274796@qq.com',
                'sender_password': 'bfbwimtwngqybbbj',
                'receiver_email': '1004274796@qq.com'
            },
            'scraping': {
                'update_interval_hours': 1,
                'max_articles_per_send': 30,
                'enable_auto_scraping': False
            },
            'ui': {
                'theme': 'light',
                'font_size': 'medium',
                'notifications_enabled': True
            }
        }
        
        self.init_mobile_storage()
    
    def init_mobile_storage(self):
        """初始化移动端存储"""
        try:
            if platform == 'android':
                try:
                    from android.storage import primary_external_storage_path  # type: ignore
                    external_path = primary_external_storage_path()
                    config_dir = Path(external_path) / 'AI资讯智能体'
                    config_dir.mkdir(exist_ok=True)
                    config_file = config_dir / 'config.json'
                except ImportError:
                    # Android模块不可用时回退到当前目录
                    config_file = Path('./mobile_config.json')
            else:
                # 桌面平台使用当前目录
                config_file = Path('./mobile_config.json')
            
            self.config_store = JsonStore(str(config_file))
            
            # 如果配置文件不存在，写入默认配置
            if not self.config_store.exists('app_config'):
                self.save_config(self.default_config)
                self.logger.info("创建默认移动端配置")
            
        except Exception as e:
            self.logger.error(f"初始化移动端存储失败: {e}")
            # 回退到内存存储
            self.config_store = JsonStore(':memory:')
            self.save_config(self.default_config)
    
    def get_config(self, section: str | None = None, key: str | None = None) -> Any:
        """获取配置"""
        try:
            if self.config_store is None:
                return self.default_config
            
            config = self.config_store.get('app_config')
            
            if section is None:
                return config
            
            if section not in config:
                return self.default_config.get(section, {})
            
            if key is None:
                return config[section]
            
            return config[section].get(key, self.default_config.get(section, {}).get(key))
            
        except Exception as e:
            self.logger.error(f"获取配置失败: {e}")
            if section and key:
                return self.default_config.get(section, {}).get(key)
            elif section:
                return self.default_config.get(section, {})
            else:
                return self.default_config
    
    def save_config(self, config: Dict[str, Any]):
        """保存配置"""
        try:
            if self.config_store is None:
                self.logger.error("配置存储未初始化")
                return
            
            self.config_store.put('app_config', **config)
            self.logger.info("移动端配置保存成功")
        except Exception as e:
            self.logger.error(f"保存配置失败: {e}")
    
    def update_config(self, section: str, key: str, value: Any):
        """更新单个配置项"""
        try:
            config = self.get_config()
            if section not in config:
                config[section] = {}
            config[section][key] = value
            self.save_config(config)
        except Exception as e:
            self.logger.error(f"更新配置失败: {e}")
    
    def get_database_path(self) -> str:
        """获取数据库文件路径"""
        try:
            if platform == 'android':
                try:
                    from android.storage import primary_external_storage_path  # type: ignore
                    external_path = primary_external_storage_path()
                    db_dir = Path(external_path) / 'AI资讯智能体'
                    db_dir.mkdir(exist_ok=True)
                    return str(db_dir / 'ai_news_mobile.db')
                except ImportError:
                    return 'ai_news_mobile.db'
            else:
                return 'ai_news_mobile.db'
        except Exception as e:
            self.logger.error(f"获取数据库路径失败: {e}")
            return 'ai_news_mobile.db'
    
    def check_network_permission(self) -> bool:
        """检查网络权限"""
        try:
            if platform == 'android':
                try:
                    from android.permissions import request_permission, Permission  # type: ignore
                    # 请求网络权限
                    request_permission(Permission.INTERNET)
                    request_permission(Permission.ACCESS_NETWORK_STATE)
                    return True
                except ImportError:
                    return True
            else:
                return True
        except Exception as e:
            self.logger.error(f"检查网络权限失败: {e}")
            return False
    
    def check_storage_permission(self) -> bool:
        """检查存储权限"""
        try:
            if platform == 'android':
                try:
                    from android.permissions import request_permission, Permission  # type: ignore
                    request_permission(Permission.WRITE_EXTERNAL_STORAGE)
                    request_permission(Permission.READ_EXTERNAL_STORAGE)
                    return True
                except ImportError:
                    return True
            else:
                return True
        except Exception as e:
            self.logger.error(f"检查存储权限失败: {e}")
            return False
    
    def get_app_info(self) -> Dict[str, str]:
        """获取应用信息"""
        return {
            'version': '1.0.0',
            'platform': platform,
            'config_path': str(self.config_store.filename) if (self.config_store and hasattr(self.config_store, 'filename')) else '内存存储',
            'database_path': self.get_database_path()
        }


class MobileNotificationManager:
    """移动端通知管理器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.plyer_available = False
        
        try:
            from plyer import notification  # type: ignore
            self.notification = notification
            self.plyer_available = True
        except ImportError:
            self.logger.warning("Plyer库不可用，通知功能将被禁用")
    
    def send_notification(self, title: str, message: str, timeout: int = 10):
        """发送通知"""
        if not self.plyer_available:
            self.logger.info(f"通知: {title} - {message}")
            return
        
        try:
            self.notification.notify(
                title=title,
                message=message,
                timeout=timeout,
                app_name='AI资讯智能体'
            )
        except Exception as e:
            self.logger.error(f"发送通知失败: {e}")
    
    def notify_new_articles(self, count: int):
        """通知新文章"""
        self.send_notification(
            title="🤖 AI资讯智能体",
            message=f"发现 {count} 篇新的AI资讯文章！",
            timeout=15
        )
    
    def notify_scraping_complete(self, count: int):
        """通知抓取完成"""
        self.send_notification(
            title="✅ 抓取完成",
            message=f"成功抓取 {count} 篇文章",
            timeout=10
        )
    
    def notify_email_sent(self, success: bool, count: int = 0):
        """通知邮件发送结果"""
        if success:
            self.send_notification(
                title="📧 邮件发送成功",
                message=f"已发送包含 {count} 篇文章的邮件",
                timeout=10
            )
        else:
            self.send_notification(
                title="❌ 邮件发送失败",
                message="请检查网络连接和邮件配置",
                timeout=15
            )


if __name__ == "__main__":
    # 测试移动端配置管理器
    print("测试移动端配置管理器...")
    
    config_manager = MobileConfigManager()
    
    # 测试获取配置
    email_config = config_manager.get_config('email')
    print(f"邮件配置: {email_config}")
    
    # 测试更新配置
    config_manager.update_config('scraping', 'update_interval_hours', 2)
    updated_config = config_manager.get_config('scraping', 'update_interval_hours')
    print(f"更新后的抓取间隔: {updated_config}")
    
    # 测试应用信息
    app_info = config_manager.get_app_info()
    print(f"应用信息: {app_info}")
    
    # 测试通知管理器
    print("\\n测试通知管理器...")
    notification_manager = MobileNotificationManager()
    notification_manager.notify_new_articles(5)
    notification_manager.notify_scraping_complete(10)
    notification_manager.notify_email_sent(True, 8)