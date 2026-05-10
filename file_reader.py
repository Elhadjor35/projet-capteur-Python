#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 14:58:56 2026

@author: elhadj
"""

from PySide6.QtWidgets import QApplication, QVBoxLayout, QComboBox, QLabel, QFileDialog
from PySide6.QtCore import Signal, Slot
import pyqtgraph as pg
import numpy as np
import sys
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

        self.selector = QComboBox()
        self.selector.addItems(["Temperature", "Humidity", "Luminosity"])

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
        self.stats = (f"Stats:\t\t\t\tMinimum\t\tMaximum\t\tMean\n"
                      f"Temperature:\t\t\t{self.temp_min:.1f}\t\t\t{self.temp_max:.1f}\t\t\t{self.temp_mean:.1f}\n"
                      f"Humidity:\t\t\t{self.hum_min:.1f}\t\t\t{self.hum_max:.1f}\t\t\t{self.hum_mean:.1f}\n"
                      f"Luminosity:\t\t\t{self.lum_min:.1f}\t\t\t{self.lum_max:.1f}\t\t\t{self.lum_mean:.1f}\n")
        self.statsWidget = QLabel(
            self.stats)

        self.graph = Graph(self.choice, self.df, self.file, self.stats)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.selector)
        layout.addWidget(self.graph)
        layout.addWidget(self.statsWidget)

    def choice_changed(self, s):
        self.graph.update_choice(s)

    def get_data(self):
        try:
            self.file = QFileDialog.getOpenFileName(self,

                                                    "Open File", os.getcwd(), "Text Files (*.txt)")

            assert self.file[0][-3:].lower() == 'txt'
        except AssertionError:
            print('No file selected')
            sys.exit()

        try:
            df = pd.read_table(
                self.file[0], sep='\s+',
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

        x0, x1 = self.lr.getRegion()

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
            self.stats = (f"Stats:\t\t\t\tMinimum\t\tMaximum\t\tMean\n"
                          f"Temperature:\t\t\t{self.temp_min:.1f}\t\t\t{self.temp_max:.1f}\t\t\t{self.temp_mean:.1f}\n"
                          f"Humidity:\t\t\t{self.hum_min:.1f}\t\t\t{self.hum_max:.1f}\t\t\t{self.hum_mean:.1f}\n"
                          f"Luminosity:\t\t\t{self.lum_min:.1f}\t\t\t{self.lum_max:.1f}\t\t\t{self.lum_mean:.1f}\n")
        except ValueError:
            pass

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

        self.curve.setData(self.timestamps, data)
