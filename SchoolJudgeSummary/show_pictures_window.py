# -- coding:utf-8 --

import sys
from PyQt5.QtCore import Qt, QSize,  QTimer, QRect
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import midway_summary_window
import summary_window
import globals

form_show_pictures, base_show_pictures = uic.loadUiType('show_pictures_window.ui')


class ShowPicturesMainPage(base_show_pictures, form_show_pictures):
    def __init__(self):
        super(base_show_pictures, self).__init__()
        self.setupUi(self)
        self._cur_picture_index = 0

        self._set_pictures()
        self.timer = QTimer()
        self.timer.timeout.connect(self._set_pictures)
        self.timer.start(937)

    def _set_pictures(self):
        self._cur_picture_index += 1
        if self._cur_picture_index > 16:
            self.timer.stop()
            if globals.display_index == 4:
                globals.cur_window = summary_window.SummaryMainPage()
                globals.cur_window.showFullScreen()
                globals.cur_window.setFocus()
            else:
                globals.cur_window = midway_summary_window.MidwaySummaryMainPage()
                globals.cur_window.showFullScreen()
                globals.cur_window.setFocus()
            self.close()
            return

        labels_coordinates = []
        margin = int(globals.screen_height / 20)
        label_height = globals.screen_height - margin * 2
        label_width = label_height

        label = self.label_1
        x = (globals.screen_width - label_width) / 2
        y = (globals.screen_height - label_height) / 2
        labels_coordinates.append([x, y])
        label.setGeometry(QRect(x, y, label_width, label_height))
        preceding = '0' if self._cur_picture_index < 10 else ''
        label_pixmap = QPixmap('res/pictures/%i/%s%i.jpg' % (globals.display_index, preceding, self._cur_picture_index))
        label_pixmap = label_pixmap.scaled(QSize(label_width, label_height))
        label.setAlignment(Qt.AlignCenter)
        label.setPixmap(label_pixmap)

    def keyPressEvent(self, evt):
        if evt.key() == Qt.Key_Escape:
            sys.exit(0)
