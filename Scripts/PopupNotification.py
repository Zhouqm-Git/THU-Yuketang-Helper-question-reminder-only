import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QPalette, QColor
import threading

class PopupNotification(QWidget):
    """
    弹窗通知类，专门用于答题提醒
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFixedSize(400, 120)  # 增大尺寸使其更醒目
        
        # 设置样式
        self.setup_ui()
        
        # 动画效果
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(500)  # 增加动画时长
        self.animation.setEasingCurve(QEasingCurve.OutBounce)  # 使用弹跳效果
        
        # 自动关闭定时器
        self.close_timer = QTimer()
        self.close_timer.timeout.connect(self.hide_notification)
        
    def setup_ui(self):
        """设置UI界面"""
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 15, 20, 15)
        
        # 标题标签
        self.title_label = QLabel("🔔 雨课堂答题提醒")
        self.title_label.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        self.title_label.setStyleSheet("color: #e74c3c; margin-bottom: 8px;")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        
        # 消息标签
        self.message_label = QLabel("")
        self.message_label.setFont(QFont("Microsoft YaHei", 12))
        self.message_label.setWordWrap(True)
        self.message_label.setStyleSheet("color: #2c3e50; line-height: 1.6; font-weight: bold;")
        self.message_label.setAlignment(QtCore.Qt.AlignCenter)
        
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.message_label)
        
        self.setLayout(main_layout)
        
        # 设置窗口样式 - 更醒目的设计
        self.setStyleSheet("""
            PopupNotification {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border: 3px solid #e74c3c;
                border-radius: 15px;
            }
        """)
        
        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)
        
    def show_notification(self, message, notification_type=3, duration=5000):
        """
        显示通知 - 专门用于答题提醒
        :param message: 通知消息
        :param notification_type: 通知类型（固定为3-收到题目）
        :param duration: 显示时长(毫秒)
        """
        self.message_label.setText(message)
        
        # 计算显示位置（屏幕中央）
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        
        # 设置初始位置（从上方滑入）
        start_rect = QRect(x, -self.height(), self.width(), self.height())
        end_rect = QRect(x, y, self.width(), self.height())
        
        self.setGeometry(start_rect)
        self.show()
        
        # 滑入动画
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.start()
        
        # 设置自动关闭
        self.close_timer.start(duration)
        
    def hide_notification(self):
        """隐藏通知"""
        self.close_timer.stop()
        
        # 淡出效果
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(300)
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.finished.connect(self.hide)
        self.fade_animation.start()
        
    def mousePressEvent(self, event):
        """点击关闭通知"""
        if event.button() == QtCore.Qt.LeftButton:
            self.hide_notification()


# 全局通知管理器
class NotificationManager:
    """通知管理器，专门管理答题提醒通知"""
    
    def __init__(self):
        self.current_notification = None
        
    def show_notification(self, message, notification_type=3, duration=5000):
        """显示答题提醒通知"""
        # 如果已有通知在显示，先关闭它
        if self.current_notification and self.current_notification.isVisible():
            self.current_notification.hide()
            
        # 创建新通知
        self.current_notification = PopupNotification()
        self.current_notification.show_notification(message, notification_type, duration)
        
        # 设置关闭回调
        def on_close():
            self.current_notification = None
            
        self.current_notification.close_timer.timeout.connect(on_close)


# 全局通知管理器实例
notification_manager = NotificationManager()

def show_popup_notification(message, notification_type=3, duration=5000):
    """
    显示答题提醒弹窗的便捷函数
    :param message: 通知消息
    :param notification_type: 通知类型（固定为3-收到题目）
    :param duration: 显示时长(毫秒)
    """
    # 在主线程中显示通知
    def show_in_main_thread():
        notification_manager.show_notification(message, notification_type, duration)
    
    # 如果在非主线程中调用，需要使用QTimer在主线程中执行
    if threading.current_thread() != threading.main_thread():
        QTimer.singleShot(0, show_in_main_thread)
    else:
        show_in_main_thread()