#!/usr/bin/env python
# -*- coding:utf-8 -*-

from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
import smtplib

# 格式化邮件地址
# def _format_addr(s):
#     name, addr = parseaddr(s)
#     return formataddr((Header(name, 'utf-8').encode(),addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def send(from_email, to_email, result):
    # 发送地址
    from_addr = from_email
    # SMTP服务
    smtp_server = '10.10.0.6'
    # 接收地址
    to_addr = to_email

    msg = MIMEMultipart()
    # 发送人
    msg['From'] = from_addr
    # 接收人
    msg['To'] = ",".join(to_addr)
    # 主题
    msg['Subject'] = u"测试结果"
    # 内容
    msg.attach(MIMEText(result, 'plain', 'utf-8'))

    try:
        # 开启SMTP协议，默认端口是25
        server = smtplib.SMTP(smtp_server,25)
        server.set_debuglevel(1)
        # 发送
        server.sendmail(from_addr,to_addr,msg.as_string())
        # 关闭
        server.quit()
        return 1
    except Exception,e:
        return 0

# def send(email, result):
#     # 发送地址
#     from_addr = 'wshnzg@sina.com'
#     password = 'lz123456789'
#     # SMTP服务
#     smtp_server = 'smtp.sina.com'
#     # 接收地址
#     to_addr = email
#
#     msg = MIMEMultipart()
#     # 发送人
#     msg['From'] = _format_addr(u'接口测试平台 <%s>' % from_addr)
#     # 接收人
#     msg['To'] = _format_addr(u'%s <%s>' % (to_addr, to_addr))
#     # 主题
#     msg['Subject'] = Header(u'测试结果', 'utf-8').encode()
#     # 内容
#     msg.attach(MIMEText(result, 'plain', 'utf-8'))
#
#     try:
#         # 开启SMTP协议，默认端口是25
#         server = smtplib.SMTP(smtp_server,25)
#         # 打印出和SMTP服务器交互的所有信息
#         server.set_debuglevel(1)
#         # 登录
#         server.login(from_addr,password)
#         # 发送
#         server.sendmail(from_addr,[to_addr],msg.as_string())
#         # 关闭
#         server.quit()
#         return 1
#     except Exception,e:
#         print e
#         return 0