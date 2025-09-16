#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
工具函数 - 仅保留答题提醒功能需要的函数
"""

import json
import urllib3
import requests
import os
import sys
from Scripts.PopupNotification import show_popup_notification

def dict_result(text):
    """json string 转 dict object"""
    return dict(json.loads(text))

def show_notification(text, notification_type=0):
    """弹窗通知函数"""
    show_popup_notification(text, notification_type)

def test_network():
    """网络状态测试"""
    try:
        http = urllib3.PoolManager()
        http.request('GET', 'https://baidu.com')
        return True
    except:
        return False

def get_initial_data():
    """获取默认配置信息 - 仅答题提醒相关"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except:
        # 默认配置
        initial_data = {
            "sessionid": "",
            "auto_answer": False,  # 关闭自动答题
            "delay_mode": "question_time",  # 使用题目时间
            "custom_delay": 10,
            "random_delay_range": 5,
            "show_popup": True  # 显示答题提醒弹窗
        }
        return initial_data

def get_user_info(sessionid):
    """获取用户信息"""
    headers = {
        "Cookie": "sessionid=%s" % sessionid,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    }
    r = requests.get(url="https://pro.yuketang.cn/api/v3/user/basic-info", headers=headers, proxies={"http": None, "https": None})
    rtn = dict_result(r.text)
    return (rtn["code"], rtn["data"])

def get_on_lesson(sessionid):
    """获取用户当前正在上课列表"""
    headers = {
        "Cookie": "sessionid=%s" % sessionid,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    }
    r = requests.get("https://pro.yuketang.cn/api/v3/classroom/on-lesson", headers=headers, proxies={"http": None, "https": None})
    rtn = dict_result(r.text)
    return (rtn["code"], rtn["data"]["onLessonClassrooms"])

def get_on_lesson_old(sessionid):
    """获取用户当前正在上课的列表（旧版）"""
    headers = {
        "Cookie": "sessionid=%s" % sessionid,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    }
    r = requests.get("https://pro.yuketang.cn/v/course_meta/on_lesson_courses", headers=headers, proxies={"http": None, "https": None})
    rtn = dict_result(r.text)
    return rtn["on_lessons"]

def resource_path(relative_path):
    """解决打包exe的图片路径问题"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_config_path():
    """获取配置文件路径"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.json')