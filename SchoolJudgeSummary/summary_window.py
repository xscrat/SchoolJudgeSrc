# -- coding:utf-8 --

import sys
from PyQt5.QtCore import Qt
import requests
from PyQt5 import uic
import globals
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from mplcanvas import MplCanvas

form_summary, base_summary = uic.loadUiType('summary_window.ui')


class SummaryMainPage(base_summary, form_summary):
    def __init__(self):
        super(base_summary, self).__init__()
        self.setupUi(self)

        r = requests.get('http://%s:%s/get_results/' % (globals.server_ip, globals.server_port))
        if r.status_code == 200:
            results = r.json()
            results = sorted(results.items(), key=lambda item: item[1], reverse=True)

            results_keys = []
            results_values = []
            for result in results:
                results_keys.append('《' + result[0] + '》')
                results_values.append(result[1])

            if len(results_keys) < 5:
                for i in range(5 - len(results_keys)):
                    results_keys.append('')
                    results_values.append(0)

            print(results_keys)
            print(results_values)

            x_list = (list(range(len(results_keys))))
            sc = MplCanvas(self.widget, width=globals.screen_width * 3 / 4, height=globals.screen_height * 4 / 5, dpi=100)
            sc_width = globals.screen_width * 5 / 6
            sc_height = globals.screen_height * 5 / 6
            sc.setGeometry((globals.screen_width - sc_width) / 2, (globals.screen_height - sc_height) / 2, sc_width, sc_height)
            sc.axes.set_position([0.1, 0.1, 0.8, 0.8])
            sc.axes.set_yticks(x_list)
            sc.axes.set_yticklabels(results_keys)
            for i, v in enumerate(results_values):
                sc.axes.text(v + .2, i + .25, str(v), color='blue', fontweight='bold')
            sc.axes.invert_yaxis()
            bar_list = sc.axes.barh(x_list, results_values)
            bar_list[0].set_color('orangered')
            bar_list[1].set_color('yellow')
            bar_list[2].set_color('cyan')
            self.widget.setGeometry(0, 0, globals.screen_width, globals.screen_height)
            sc.setParent(self.widget)

    def keyPressEvent(self, evt):
        if evt.key() == Qt.Key_Escape:
            sys.exit(0)
