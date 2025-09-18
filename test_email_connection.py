#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件连接诊断脚本
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from email_sender import EmailSender
import smtplib
import configparser

def test_smtp_connection():
    """测试SMTP连接"""
    print("🔍 测试SMTP连接")
    print("=" * 40)
    
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    
    smtp_server = config.get('email', 'smtp_server')
    smtp_port = int(config.get('email', 'smtp_port'))
    sender_email = config.get('email', 'sender_email')
    sender_password = config.get('email', 'sender_password')
    
    print(f"服务器: {smtp_server}")
    print(f"端口: {smtp_port}")
    print(f"邮箱: {sender_email}")
    print(f"授权码: {'*' * len(sender_password)}")
    
    try:
        print("\n🔌 尝试连接SMTP服务器...")
        with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=30) as server:
            print("✅ SSL连接成功")
            
            print("🔐 尝试登录...")
            server.login(sender_email, sender_password)
            print("✅ 登录成功")
            
            print("✅ SMTP连接测试通过")
            return True
            
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ 认证失败: {e}")
        print("💡 请检查:")
        print("   • QQ邮箱是否开启了SMTP服务")
        print("   • 是否使用了正确的授权码（不是登录密码）")
        return False
        
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False

def test_send_simple_email():
    """发送简单测试邮件"""
    print("\n📧 发送简单测试邮件")
    print("=" * 40)
    
    email_sender = EmailSender()
    success = email_sender.send_test_email()
    
    if success:
        print("✅ 测试邮件发送成功")
    else:
        print("❌ 测试邮件发送失败")
    
    return success

if __name__ == "__main__":
    print("🧪 邮件功能完整诊断")
    print("=" * 50)
    
    # 测试1: SMTP连接
    connection_ok = test_smtp_connection()
    
    if connection_ok:
        # 测试2: 发送邮件
        send_ok = test_send_simple_email()
        
        if send_ok:
            print("\n🎉 邮件功能正常！")
            print("现在可以测试包含文章总结的邮件发送了。")
        else:
            print("\n⚠️ 连接正常但发送失败，请检查邮件内容格式")
    else:
        print("\n❌ 连接失败，请检查配置")
        print("\n💡 QQ邮箱配置指南:")
        print("1. 登录QQ邮箱网页版")
        print("2. 设置 -> 账户")
        print("3. 开启 SMTP 服务")
        print("4. 生成授权码")
        print("5. 在config.ini中使用授权码替换密码")