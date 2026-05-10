# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 20:21:22 2026

@author: Majdo
"""
from PySide6.QtWidgets import QApplication, QVBoxLayout, QComboBox, QLabel, QFileDialog, QPushButton
from PySide6.QtCore import QThread, Signal, Slot
import pyqtgraph as pg
import numpy as np
import time
from serial_reader import read_serial
from data_logger import save_data
import os
import sys


class MainWindow(pg.GraphicsLayoutWidget):
    def __init__(self, Graph):
        super().__init__(parent=None)
        self.pick_file()
        self.setup_ui()
        self.worker = Worker()
        self.make_connection_worker(self.worker)

        self.worker.start()

    def setup_ui(self):
        self.setWindowTitle("Sensor")

        self.selector = QComboBox()
        self.selector.addItems(["Temperature", "Humidity", "Luminosity"])

        self.choice = self.selector.currentText()
        self.selector.currentTextChanged.connect(self.choice_changed)
        self.modes = QComboBox()
        self.modes.addItems(["Simulation", "Real"])

        self.mode = self.modes.currentText()
        self.modes.currentTextChanged.connect(self.mode_changed)
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

        self.graph = Graph(self.choice, self.mode, self.file, self.stats)
        self.saving = False
        self.button = QPushButton(f"Saving: {self.saving}", self)

        self.button.clicked.connect(self.switch_save)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.selector)
        layout.addWidget(self.modes)
        layout.addWidget(self.button)
        layout.addWidget(self.graph)
        layout.addWidget(self.statsWidget)

    def switch_save(self):

        self.saving = not self.saving
        self.button.setText(f"Saving: {self.saving}")

    def choice_changed(self, s):
        self.graph.update_choice(s)

    def mode_changed(self, s):

        self.worker.change_mode(s)

    def closeEvent(self, event):
        self.worker.stop()
        QApplication.quit()

    def pick_file(self):
        try:
            self.file = QFileDialog.getSaveFileName(self,

                                                    "Save File", os.getcwd(), "Text Files (*.txt)")
            assert len(self.file[0]) > 0

        except AssertionError:
            print("No file selected")
            sys.exit()

    def make_connection_worker(self, data_object):
        data_object.signal.connect(self.grab_data)

    @Slot(object)
    def grab_data(self, d):
        data = {"Time": d[0], "Temperature": d[1],
                "Humidity": d[2], "Luminosity": d[3]}
        self.graph.update_curve(data)

        if self.saving:

            try:
                save_data(
                    self.file[0], d[0], d[1], d[2], d[3])
            except FileNotFoundError:
                sys.exit()
        self.statsWidget.setText(self.graph.updateStats())

    def update_stats(self, stats):
        self.stats = stats

        self.statsWidget.setText(self.stats)


class Graph(pg.PlotWidget):

    def __init__(self, choice, mode, file, stats):
        super().__init__(parent=None)
        self.setTitle(file[0])
        self.setAxisItems(axisItems={"bottom": pg.DateAxisItem()})
        self.abscissa = self.setLabel("bottom", "Time")
        self.ordinate = self.setLabel("left", "Temperature", "°C")
        self.curve = self.plot(pen="y")
        self.timestamps = []
        self.temp = np.zeros(30)
        self.hum = np.zeros(30)
        self.lum = np.zeros(30)
        self.mode = mode
        self.choice = choice
        self.update_choice(self.choice)
        self.data0 = {
            "Time": time.time(),
            "Temperature": 0,
            "Humidity": 0,
            "Luminosity": 0,
        }
        self.update_curve(self.data0)
        self.stats = stats

    def update_choice(self, s):

        self.removeItem(self.ordinate)
        if s == "Temperature":
            self.ordinate = self.setLabel("left", s, "°C")
            self.setYRange(0, 35)
        elif s == "Humidity":
            self.ordinate = self.setLabel("left", s, "%")
            self.setYRange(0, 100)
        else:
            self.ordinate = self.setLabel("left", s, "%")
            self.setYRange(0, 100)
        self.choice = s

    def switch_save(self):

        self.saving = not self.saving
        self.button.setText(f"Saving: {self.saving}")

    def updateStats(self):

        try:
            self.temp_min = np.nanmin(
                self.temp)
            self.temp_max = np.nanmax(
                self.temp)
            self.temp_mean = np.nanmean(
                self.temp)
            self.hum_min = np.nanmin(
                self.hum)
            self.hum_max = np.nanmax(
                self.hum)
            self.hum_mean = np.nanmean(
                self.hum)
            self.lum_min = np.nanmin(
                self.lum)
            self.lum_max = np.nanmax(
                self.lum)
            self.lum_mean = np.nanmean(
                self.lum)

            self.stats = (f"Stats:\t\t\t\tMinimum\t\tMaximum\t\tMean\n"
                          f"Temperature:\t\t\t{self.temp_min:.1f}\t\t\t{self.temp_max:.1f}\t\t\t{self.temp_mean:.1f}\n"
                          f"Humidity:\t\t\t{self.hum_min:.1f}\t\t\t{self.hum_max:.1f}\t\t\t{self.hum_mean:.1f}\n"
                          f"Luminosity:\t\t\t{self.lum_min:.1f}\t\t\t{self.lum_max:.1f}\t\t\t{self.lum_mean:.1f}\n")
        except ValueError as e:
            print(e)
            pass
        return self.stats

    def update_curve(self, d):
        timestamp = d["Time"]
        self.timestamps = 0.5 * np.linspace(timestamp - 58.01, timestamp, 30)

        self.temp[-1] = d["Temperature"]
        self.hum[-1] = d["Humidity"]
        self.lum[-1] = d["Luminosity"]
        self.temp[:-1] = self.temp[1:]
        self.hum[:-1] = self.hum[1:]
        self.lum[:-1] = self.lum[1:]
        if self.choice == "Temperature":
            data = self.temp
        elif self.choice == "Humidity":
            data = self.hum
        elif self.choice == "Luminosity":
            data = self.lum
        self.curve.setData(self.timestamps, data)

        self.curve.setPos(self.timestamps[0], 0)


class Worker(QThread):
    signal = Signal(object)

    def __init__(self):
        super().__init__()
        self.mode = 'Simulation'
        self.keepRunning = True

    def run(self):
        self.data = []

        while self.keepRunning:
            a = self.mode
            if not self.keepRunning:

                break

            for line in read_serial(a):
                if a != self.mode:

                    break

                if not self.keepRunning:

                    break
                try:
                    parts = [float(i) for i in line.split(" ")]

                    timestamp, temp, hum, lum = parts[0], parts[1], parts[2], parts[3]
                except AttributeError:

                    self.stop()

                except ValueError:
                    print("Erreur conversion :", line)
                    self.stop()
                self.data = [timestamp, temp, hum, lum]

                self.signal.emit(self.data)

    def change_mode(self, m):

        self.mode = m

        self.keepRunning = True

    def stop(self):
        self.keepRunning = False
