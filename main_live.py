# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 20:22:22 2026

@author: Majdo
"""
if __name__ == '__main__':
    from realtime_plot import MainWindow, Graph, Worker

    import sys
    from PySide6.QtWidgets import QApplication
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    widget = MainWindow(Graph)
    widget.show()
    sys.exit(app.exec())
