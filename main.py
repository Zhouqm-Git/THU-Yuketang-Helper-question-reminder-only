#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
雨课堂答题提醒助手 - 主程序入口
仅提供答题提醒功能，不进行自动答题
"""

import sys
from PyQt5 import QtWidgets
from UI.MainWindow import MainWindow_Ui

if __name__ == "__main__":
    # 初始化应用程序
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("雨课堂答题提醒助手")
    app.setApplicationVersion("1.0")
    
    # 创建主窗口
    main = QtWidgets.QMainWindow()
    ui = MainWindow_Ui()
    ui.setupUi(main)
    main.show()
    
    # 启动应用程序主循环
    sys.exit(app.exec_())

