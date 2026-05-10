#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 14:58:56 2026

@author: elhadj
"""

from PySide6.QtWidgets import QApplication, QVBoxLayout, QComboBox, QLabel, QFileDialog, QGraphicsTextItem
from PySide6.QtCore import QThread, Signal, Slot
import pyqtgraph as pg
import numpy as np
import time
import pandas as pd
import os


class MainWindow(pg.GraphicsLayoutWidget):
    def __init__(self, Graph):
        super().__init__(parent=None)

        self.get_data()
        self.setup_ui()
        self.make_connection(self.graph)

    def setup_ui(self):
        self.setWindowTitle("Sensor")
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.selector = QComboBox()
        self.selector.addItems(["Temperature", "Humidity", "Luminosity"])
        layout.addWidget(self.selector)
        self.choice = self.selector.currentText()
        self.selector.currentTextChanged.connect(self.choice_changed)

        self.temp_min = 0
        self.temp_max = 0
        self.temp_mean = 0
        self.hum_min = 0
        self.hum_max = 0
        self.hum_mean = 0
        self.lum_min = 0
        self.lum_max = 0
        self.lum_mean = 0
        self.stats = f"Stats:\t\t\t\tMinimum\t\tMaximum\t\tMean\nTemperature (°C):\t\t\t{self.temp_min:.1f}\t\t\t{self.temp_max:.1f}\t\t\t{self.temp_mean:.1f}\nHumidity (%):\t\t\t{self.hum_min:.1f}\t\t\t{self.hum_max:.1f}\t\t\t{self.hum_mean:.1f}\nLuminosity (%):\t\t\t{self.lum_min:.1f}\t\t\t{self.lum_max:.1f}\t\t\t{self.lum_mean:.1f}\n"
        self.statsWidget = QLabel(
            self.stats)
        # layout.addWidget(self.stats_label)
        # self.text = pg.TextItem(
        #     # f"Min: {y_min}\nMax: {y_max}\nMoy: {y_mean:.2f}"
        #     text="fssd", color='w')
        self.graph = Graph(self.choice, self.df, self.file, self.stats)
        layout.addWidget(self.graph)
        layout.addWidget(self.statsWidget)

    def choice_changed(self, s):
        self.graph.update_choice(s)

    def get_data(self):
        try:
            self.file = QFileDialog.getOpenFileName(self,
                                                    # '28030254.TXT'
                                                    # , "Text Files (*.txt *.csv)")
                                                    "Open File", os.getcwd(), "Text Files (*.txt)")
        # print(file[0])
            assert self.file[0][-3:].lower() == 'txt'
        except AssertionError:
            print('No file selected')
            # sys.exit()
        try:
            df = pd.read_table(
                self.file[0], sep='\s+',  # Choisir le nom du fichier
                names=['day', 'month', 'year', 'hour',
                       'minute', 'second', "Temperature", "Humidity", "Luminosity"],
                header=0, parse_dates={'Time': ['day', 'month', 'year', 'hour',
                                                'minute', 'second']},
                date_format={'Time': '%d %m %y %H %M %S'})
            df2 = df.drop(df[(df["Temperature"] == 0) & (df["Luminosity"] == 0)
                             & (df["Humidity"] == 0)].index).reset_index()
            df3 = df2
            df3['Time'] = df2['Time'].dt.tz_localize(tz='Europe/Paris')
            df3['Time_unix'] = pd.to_datetime(df3['Time']).astype(int) / 10**9
            self.df = df3
        except pd.errors.ParserError as e:
            print("Wrong file format", e)
            sys.exit()

    def make_connection(self, stats):
        stats.signal.connect(self.update_stats)

    @Slot(object)
    def update_stats(self, stats):
        self.stats = stats
        print(self.stats)
        self.statsWidget.setText(self.stats)

    def closeEvent(self, event):
        QApplication.quit()


class Graph(pg.PlotWidget):
    signal = Signal(object)

    def __init__(self, choice, df, file, stats):
        super().__init__(parent=None)
        self.setTitle = self.setTitle(file[0])
        self.setAxisItems(axisItems={"bottom": pg.DateAxisItem()})
        self.abscissa = self.setLabel("bottom", "Time")
        self.ordinate = self.setLabel("left", "Temperature", "°C")
        self.curve = self.plot(pen="y")
        self.df = df
        self.timestamps = df['Time_unix']
        self.temp = df['Temperature']
        self.hum = df['Humidity']
        self.lum = df['Luminosity']
        self.choice = choice
        self.update_choice(self.choice)
        self.lr = pg.LinearRegionItem(
            [self.timestamps[0], self.timestamps[0]+100])
        self.lr.sigRegionChanged.connect(self.updateStats)
        self.addItem(self.lr)
        self.stats = stats

    def updateStats(self):
        x = self.timestamps
        t = self.temp
        h = self.hum
        l = self.lum
        # print(lr.getRegion(), type(lr.getRegion()))
        # print(np.mean())
        # print(list(x))
        # print(list(y))
        x0, x1 = self.lr.getRegion()
        # print(lo, hi)
       # h = y[list(x).index(round(x0)):list(x).index(round(x1))]
        # print(list(x).index(round(lo)))
        try:
            self.temp_min = np.nanmin(
                t[list(x).index(round(x0)):list(x).index(round(x1))])
            self.temp_max = np.nanmax(
                t[list(x).index(round(x0)):list(x).index(round(x1))])
            self.temp_mean = np.nanmean(
                t[list(x).index(round(x0)):list(x).index(round(x1))])
            self.hum_min = np.nanmin(
                h[list(x).index(round(x0)):list(x).index(round(x1))])
            self.hum_max = np.nanmax(
                h[list(x).index(round(x0)):list(x).index(round(x1))])
            self.hum_mean = np.nanmean(
                h[list(x).index(round(x0)):list(x).index(round(x1))])
            self.lum_min = np.nanmin(
                l[list(x).index(round(x0)):list(x).index(round(x1))])
            self.lum_max = np.nanmax(
                l[list(x).index(round(x0)):list(x).index(round(x1))])
            self.lum_mean = np.nanmean(
                l[list(x).index(round(x0)):list(x).index(round(x1))])
            self.stats = f"Stats:\t\t\t\tMinimum\t\tMaximum\t\tMean\nTemperature:\t\t\t{self.temp_min:.1f}\t\t\t{self.temp_max:.1f}\t\t\t{self.temp_mean:.1f}\nHumidity:\t\t\t{self.hum_min:.1f}\t\t\t{self.hum_max:.1f}\t\t\t{self.hum_mean:.1f}\nLuminosity:\t\t\t{self.lum_min:.1f}\t\t\t{self.lum_max:.1f}\t\t\t{self.lum_mean:.1f}\n"
        except ValueError:
            pass
       # print(self.stats)
        self.signal.emit(self.stats)

    def update_choice(self, s):

        self.removeItem(self.ordinate)
        if s == "Temperature":
            self.ordinate = self.setLabel("left", s, "°C")
            self.setYRange(0, 35)
            data = self.temp
        elif s == "Humidity":
            self.ordinate = self.setLabel("left", s, "%")
            self.setYRange(0, 100)
            data = self.hum
        else:
            self.ordinate = self.setLabel("left", s, "%")
            self.setYRange(0, 100)
            data = self.lum
        # print(self.timestamps)
        # print(data)
        self.curve.setData(self.timestamps, data)


if __name__ == "__main__":
    import sys
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    widget = MainWindow(Graph)
    widget.show()
    sys.exit(app.exec())
# import pyqtgraph as pg
# import pandas as pd
# from pyqtgraph.Qt import QtGui, QtWidgets, mkQApp

# fichier_entree = '09021802.TXT'

# # %%
# df = pd.read_csv(fichier_entree,sep='\s+',header=0)
# print(df)
# # %%
# df2 = df.drop(df[(df["Temp"]==0) & (df["Lum"] == 0 ) & (df["Hum"]== 0)].index).reset_index()
# df3 = df2
# df3['Time']=df2['Time'].dt.tz_localize(tz='Europe/Paris')
# df3['Time_unix']=pd.to_datetime(df3['Time']).astype(int) / 10**9
# # %%
# app = pg.mkQApp()
# win = pg.GraphicsLayoutWidget(show=True, title='Données')
# win.resize(900,480)
# win.setWindowTitle('Sensors')
# p1 = win.addPlot(title="Temperature",axisItems = {'bottom': pg.DateAxisItem()})
# p1.showGrid(x=True, y=True)
# p1.plot(df3['Time_unix'], df3['Temp'])

# p2 = win.addPlot(title="Humidité",axisItems = {'bottom': pg.DateAxisItem()})
# p2.showGrid(x=True, y=True)
# p2.plot(df3['Time_unix'], df3['Hum'])

# p3 = win.addPlot(title="Luminosité",axisItems = {'bottom': pg.DateAxisItem()})
# p3.showGrid(x=True, y=True)
# p3.plot(df3['Time_unix'], df3['Lum'])
# # %%

# if __name__ == '__main__':
#     pg.exec()
