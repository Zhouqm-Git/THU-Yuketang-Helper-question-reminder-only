#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
课程类 - 仅保留答题提醒功能
"""

import requests
import websocket
import json
from Scripts.Utils import dict_result, get_initial_data
from Scripts.PopupNotification import show_popup_notification

wss_url = "wss://pro.yuketang.cn/wsapp/"

class Lesson:
    def __init__(self, lessonid, lessonname, sessionid):
        self.lessonid = lessonid
        self.lessonname = lessonname
        self.sessionid = sessionid
        self.headers = {
            "Cookie": "sessionid=%s" % self.sessionid,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
        }
        self.problems_ls = []
        self.config = get_initial_data()
        
    def _get_ppt(self, presentationid):
        """获取PPT数据"""
        url = "https://pro.yuketang.cn/api/v3/lesson/presentation/fetch?presentation_id=%s" % presentationid
        r = requests.get(url=url, headers=self.headers, proxies={"http": None, "https": None})
        return dict_result(r.text)["data"]

    def get_problems(self, presentationid):
        """获取PPT中的题目"""
        ppt_data = self._get_ppt(presentationid)
        return ppt_data.get("problems", [])

    def show_question_notification(self, problemid, problemtype, limit):
        """显示答题提醒通知"""
        # 检查是否启用弹窗提醒
        if not self.config.get('show_popup', True):
            return
            
        # 构造提醒消息
        if limit == -1:
            message = f"{self.lessonname} 检测到新题目，该题不限时"
        else:
            message = f"{self.lessonname} 检测到新题目，剩余时间 {limit} 秒"
        
        # 显示弹窗提醒
        show_popup_notification(message, 3)

    def on_open(self, wsapp):
        """WebSocket连接打开时的处理"""
        auth_data = {"op": "auth", "role": "student", "auth": self.auth}
        wsapp.send(json.dumps(auth_data))

    def checkin_class(self):
        """签到获取认证信息"""
        url = "https://pro.yuketang.cn/v2/api/lesson/checkin"
        data = {"lesson_id": self.lessonid}
        try:
            r = requests.post(url=url, headers=self.headers, data=json.dumps(data), proxies={"http": None, "https": None})
            if r.text.strip():  # 检查响应是否为空
                rtn = dict_result(r.text)
                if rtn["code"] == 0:
                    return rtn["data"]["auth"]
                else:
                    return None
            else:
                # 响应为空，可能是网络问题或API变更
                return None
        except (json.JSONDecodeError, KeyError, requests.RequestException) as e:
            # 处理JSON解析错误或网络错误
            return None

    def on_message(self, wsapp, message):
        """处理WebSocket消息 - 仅处理答题提醒"""
        data = json.loads(message)
        op = data.get("op")
        
        if op == "requestlogin":
            # 需要重新登录
            wsapp.close()
        elif op == "lessonfinished":
            # 课程结束
            wsapp.close()
        elif op == "presentationupdated":
            # PPT更新，获取新的题目列表
            self.problems_ls.extend(self.get_problems(data["presentation"]))
        elif op == "presentationcreated":
            # 新PPT创建，获取题目列表
            self.problems_ls.extend(self.get_problems(data["presentation"]))
        elif op == "problemactivated":
            # 题目激活 - 显示答题提醒
            problemid = data["problemId"]
            limit = data.get("limit", -1)
            if limit != -1:
                limit = int(limit / 1000)  # 转换为秒
            
            # 查找题目信息
            for problem in self.problems_ls:
                if problem["problemId"] == problemid:
                    self.show_question_notification(problemid, problem["problemType"], limit)
                    break
            else:
                # 如果没找到题目，发送查询请求
                self._query_problem_info(wsapp, problemid)
        elif op == "probleminfo":
            # 处理题目信息查询的返回
            if data["limit"] != -1:
                time_left = int(data["limit"] - (int(data["now"]) - int(data["dt"])) / 1000)
            else:
                time_left = data["limit"]
            
            if time_left > 0 or time_left == -1:
                self.show_question_notification(data["problemid"], data.get("problemType", 1), time_left)

    def _query_problem_info(self, wsapp, problemid):
        """查询题目详情信息"""
        query_problem = {"op": "probleminfo", "lessonid": self.lessonid, "problemid": problemid, "msgid": 1}
        wsapp.send(json.dumps(query_problem))

    def start_lesson(self, callback=None):
        """开始监听课程"""
        self.auth = self.checkin_class()
        if not self.auth:
            return None
            
        self.wsapp = websocket.WebSocketApp(
            url=wss_url, 
            header=self.headers, 
            on_open=self.on_open, 
            on_message=self.on_message
        )
        self.wsapp.run_forever()
        
        if callback:
            return callback(self)

    def get_lesson_info(self):
        """获取课程信息"""
        url = "https://pro.yuketang.cn/api/v3/lesson/basic-info"
        r = requests.get(url=url, headers=self.headers, proxies={"http": None, "https": None})
        return dict_result(r.text)["data"]

    def __eq__(self, other):
        """比较两个课程是否相同"""
        return self.lessonid == other.lessonid