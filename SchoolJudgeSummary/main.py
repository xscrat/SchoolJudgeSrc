from PyQt5.QtCore import Qt, QSize,  QTimer
from PyQt5.QtWidgets import (QApplication)
from PyQt5.QtWidgets import QMainWindow, QGraphicsOpacityEffect, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QTransform
import sys
import os
import random
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
import summary_window
import show_pictures_window
import globals
import midway_summary_window

'''
class MyMainForm(QMainWindow, Ui_MainWindow):
    signal_close_popup = pyqtSignal()

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.setWindowTitle(' ')
        # self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)

        self.all_dynamic_labels = []

        self.judge_result_table.setRowCount(2)
        self.judge_result_table.setColumnCount(2)
        self.judging_layout.removeWidget(self.judge_result_table)
        self.judge_result_table.setVisible(False)

        for dynamic_label in self.all_dynamic_labels:
            dynamic_label.setVisible(False)

        self.cur_switch = True
        self.timer = QTimer()
        self.timer.timeout.connect(self._on_timer)
        self.timer.start(2000)

    def _on_switch_display(self):
        if self.cur_switch:
            self.judging_layout.addWidget(self.judge_result_table)
            self.judging_layout.removeWidget(self.count_down_label)
            self.judging_layout.removeWidget(self.judging_label)
            self.count_down_label.setVisible(False)
            self.judging_label.setVisible(False)
            self.judge_result_table.setVisible(True)
            for dynamic_label in self.all_dynamic_labels:
                dynamic_label.setVisible(True)
        else:
            self.judging_layout.removeWidget(self.judge_result_table)
            self.judging_layout.addWidget(self.count_down_label)
            self.judging_layout.addWidget(self.judging_label)
            self.count_down_label.setVisible(True)
            self.judging_label.setVisible(True)
            self.judge_result_table.setVisible(False)
            for dynamic_label in self.all_dynamic_labels:
                dynamic_label.setVisible(False)
        self.cur_switch = not self.cur_switch

    def _on_timer(self):
        pass

    def closeEvent(self, event):
        self.timer.stop()

    def keyPressEvent(self, evt):
        if evt.key() == Qt.Key_Escape:
            sys.exit(0)
        else:
            self.main = summary_window.SummaryMainPage()
            self.main.showFullScreen()
            self.close()
            # self._on_switch_display()
'''

if __name__ == '__main__':
    if len(sys.argv[1:]) >= 1:
        globals.display_index = int(sys.argv[1])

    app = QApplication(sys.argv)
    app_icon = QIcon()
    app_icon.addFile('res/main_window_icon.jpg', QSize(16, 16))
    app.setWindowIcon(app_icon)
    screen = app.primaryScreen()
    size = screen.size()
    globals.screen_width = size.width()
    globals.screen_height = size.height()
    globals.cur_window = show_pictures_window.ShowPicturesMainPage()
    globals.cur_window.showFullScreen()
    globals.cur_window.setFocus()
    sys.exit(app.exec_())
