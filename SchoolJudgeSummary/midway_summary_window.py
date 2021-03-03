# -- coding:utf-8 --

import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QFont
import requests
from PyQt5 import uic
import globals

form_midway_summary, base_midway_summary = uic.loadUiType('midway_summary_window.ui')


class MidwaySummaryMainPage(base_midway_summary, form_midway_summary):
    def __init__(self):
        super(base_midway_summary, self).__init__()
        self.setupUi(self)
        r = requests.get('http://%s:%s/get_midway_results/%i' % (globals.server_ip, globals.server_port, globals.display_index))
        if r.status_code == 200:
            results = r.json()

            results_keys = []
            results_values = []
            for program_info in results['midway_programs_result']:
                results_keys.append('《' + program_info['name'] + '》')
                results_values.append(program_info['mark'])

            print(results_keys)
            print(results_values)

            if len(results_keys) < 5:
                for i in range(5 - len(results_keys)):
                    results_keys.append('')
                    results_values.append('')

            table_height = globals.screen_height * 4 / 5
            table_width = globals.screen_width / 2
            self.judge_result_table.setGeometry(QRect((globals.screen_width - table_width) / 2,
                                                      (globals.screen_height - table_height) / 2,
                                                      table_width,
                                                      table_height))

            font = QFont()
            font.setPointSize(26)

            row_count = 5
            self.judge_result_table.setRowCount(row_count)
            self.judge_result_table.setColumnCount(2)
            self.judge_result_table.setFocusPolicy(Qt.NoFocus)
            self.judge_result_table.setFont(font)
            self.judge_result_table.setShowGrid(False)
            self.judge_result_table.setStyleSheet('QTableView::item{border:none;background-color:white}')
            self.judge_result_table.setVerticalHeaderLabels([''] * row_count)
            self.judge_result_table.setHorizontalHeaderLabels(['节目名称', '得分'])
            for i in range(row_count):
                item = QTableWidgetItem(str(results_keys[i]))
                item.setTextAlignment(Qt.AlignCenter)
                self.judge_result_table.setItem(i, 0, item)
                item = QTableWidgetItem(str(results_values[i]))
                item.setTextAlignment(Qt.AlignCenter)
                self.judge_result_table.setItem(i, 1, item)

            font.setPointSize(26)
            horizontal_header = self.judge_result_table.horizontalHeader()
            horizontal_header.setDefaultAlignment(Qt.AlignCenter)
            horizontal_header.setSectionResizeMode(QHeaderView.Stretch)
            horizontal_header.setStyleSheet('QHeaderView::section{border:none;background-color:white;}')
            horizontal_header.setFont(font)
            font.setPointSize(26)
            vertical_header = self.judge_result_table.verticalHeader()
            vertical_header.setDefaultAlignment(Qt.AlignCenter)
            vertical_header.setSectionResizeMode(QHeaderView.Stretch)
            vertical_header.setStyleSheet('QHeaderView::section{border:none;background-color:white;}')
            vertical_header.setFont(font)

    def keyPressEvent(self, evt):
        if evt.key() == Qt.Key_Escape:
            sys.exit(0)
