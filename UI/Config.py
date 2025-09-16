#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
配置窗口 - 仅保留答题提醒功能
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Scripts.Utils import *
import json

class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("答题提醒配置")
        self.setFixedSize(350, 200)
        self.init_ui()
        self.load_config()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # 通知配置组
        notification_group = QGroupBox("通知配置")
        notification_layout = QVBoxLayout()
        
        self.show_popup_cb = QCheckBox("显示答题提醒弹窗")
        self.show_popup_cb.setChecked(True)
        notification_layout.addWidget(self.show_popup_cb)
        
        # 弹窗显示时长
        duration_widget = QWidget()
        duration_layout = QHBoxLayout()
        duration_layout.setContentsMargins(20, 0, 0, 0)
        
        duration_layout.addWidget(QLabel("弹窗显示时长:"))
        self.popup_duration_spin = QSpinBox()
        self.popup_duration_spin.setRange(1, 30)
        self.popup_duration_spin.setValue(3)
        self.popup_duration_spin.setSuffix(" 秒")
        duration_layout.addWidget(self.popup_duration_spin)
        duration_layout.addStretch()
        
        duration_widget.setLayout(duration_layout)
        notification_layout.addWidget(duration_widget)
        
        notification_group.setLayout(notification_layout)
        layout.addWidget(notification_group)
        
        # 说明文字
        info_label = QLabel("说明：本工具仅提供答题提醒功能，不进行自动答题")
        info_label.setStyleSheet("color: #666; font-size: 12px;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # 按钮
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("保存")
        self.cancel_btn = QPushButton("取消")
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        self.setLayout(layout)
        
        # 连接信号
        self.save_btn.clicked.connect(self.save_config)
        self.cancel_btn.clicked.connect(self.close)

    def load_config(self):
        """加载配置"""
        try:
            config_path = get_config_path()
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = get_initial_data()
            
            # 加载通知配置
            self.show_popup_cb.setChecked(config.get('show_popup', True))
            self.popup_duration_spin.setValue(config.get('popup_duration', 3))
            
        except Exception as e:
            print(f"加载配置失败: {e}")

    def save_config(self):
        """保存配置"""
        try:
            # 读取现有配置
            config_path = get_config_path()
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = get_initial_data()
            
            # 更新配置
            config['show_popup'] = self.show_popup_cb.isChecked()
            config['popup_duration'] = self.popup_duration_spin.value()
            
            # 保存到文件
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            QMessageBox.information(self, "成功", "配置保存成功！")
            self.close()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存配置失败: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ConfigWindow()
    window.show()
    sys.exit(app.exec_())
