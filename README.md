# 清华大学荷塘雨课堂助手（仅提醒功能版）

## 项目说明
&emsp;&emsp;本项目基于 [zhangchi2004/THU-Yuketang-Helper](https://github.com/zhangchi2004/THU-Yuketang-Helper) 进行简化修改，专注于提供答题提醒功能。

&emsp;&emsp;原项目基于 *TrickyDeath* 的项目 [RainClassroomAssistant](https://github.com/TrickyDeath/RainClassroomAssitant) 进行修改，以专门适配清华大学的荷塘雨课堂。

## 功能特点
本版本专注于提醒功能，移除了所有自动化操作：

 - ✅ **答题提醒** - 收到题目时弹窗提醒，避免错过答题
 - ✅ **课程监听** - 自动监听正在进行的课程
 - ✅ **多线程支持** - 支持同时监听多个课程
 - ✅ **简洁UI** - 保持简洁美观的用户界面
 - ❌ ~~自动签到~~ - 已移除
 - ❌ ~~自动答题~~ - 已移除  
 - ❌ ~~自动发弹幕~~ - 已移除

## 为什么选择仅提醒版本？
- **合规性** - 避免违反学术诚信规定
- **稳定性** - 专注核心功能，减少出错可能
- **轻量化** - 去除冗余功能，运行更稳定
- **实用性** - 提醒功能是最实用且合规的需求

## 使用方法
1. 下载并运行程序
2. 登录雨课堂账号
3. 程序会自动监听课程并在有题目时提醒

## 系统要求
- Windows 系统
- Python 3.7+
- 网络连接

## 安装依赖
```bash
pip install -r requirements.txt
```

## 运行程序
```bash
python main.py
```