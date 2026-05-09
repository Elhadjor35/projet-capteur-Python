# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 20:21:22 2026

@author: Majdo
"""
from PySide6.QtWidgets import QApplication, QVBoxLayout, QComboBox, QLabel, QFileDialog
from PySide6.QtCore import QThread, Signal, Slot
import pyqtgraph as pg
import numpy as np
import time
from serial_reader import read_serial
from data_logger import save_data
import os


class MainWindow(pg.GraphicsLayoutWidget):
    def __init__(self, Graph):
        super().__init__(parent=None)
        self.pick_file()
        self.setup_ui()
        self.worker = Worker()
        self.make_connection(self.worker)
        self.worker.start()

    def setup_ui(self):
        self.setWindowTitle("Sensor")
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.selector = QComboBox()
        self.selector.addItems(["Temperature", "Humidity", "Luminosity"])
        layout.addWidget(self.selector)
        self.choice = self.selector.currentText()
        self.selector.currentTextChanged.connect(self.choice_changed)
        self.modes = QComboBox()
        self.modes.addItems(["Simulation", "Real"])
        layout.addWidget(self.modes)
        self.mode = self.modes.currentText()
        self.modes.currentTextChanged.connect(self.mode_changed)

        self.graph = Graph(self.choice, self.mode, self.file)
        layout.addWidget(self.graph)
        self.stats_label = QLabel("Stats:")
        layout.addWidget(self.stats_label)

    def choice_changed(self, s):
        self.graph.update_choice(s)

    def mode_changed(self, s):
        self.graph.update_mode(s)
        self.worker.change_mode(s)

    def closeEvent(self, event):
        self.worker.stop()
        QApplication.quit()

    def pick_file(self):
        try:
            file = QFileDialog.getSaveFileName(self,
                                               # '28030254.TXT'
                                               # , "Text Files (*.txt *.csv)")
                                               "Save File", os.getcwd(), "Text Files (*.txt)")
            assert file[0][-3:].lower() == "txt"

        except AssertionError:
            print("No file selected")
            sys.exit()
        self.file = file

    def make_connection(self, data_object):
        data_object.signal.connect(self.grab_data)

    @Slot(object)
    def grab_data(self, d):
        data = {"Time": d[0], "Temperature": d[1],
                "Humidity": d[2], "Luminosity": d[3]}
        self.graph.update_curve(data)
        print(self.file[0])
        try:
            save_data(
                self.file[0], d[0], d[1], d[2], d[3])
        except FileNotFoundError:
            sys.exit
    # def closeEvent(self, event):


class Graph(pg.PlotWidget):
    def __init__(self, choice, mode, file):
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

    def update_mode(self, s):
        print(s)

    def update_choice(self, s):
        # print(s)
        # self.setTitle(s)
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

    def update_curve(self, d):
        timestamp = d["Time"]
        self.timestamps = 0.5 * np.linspace(timestamp - 58.01, timestamp, 30)
        # print(self.timestamps)
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
        # self.setTitle(self.choice)
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
            # print(a)
           # print(self.mode)
            # print('gswe')
            for line in read_serial(a):
                if a != self.mode:
                    # print('c')
                    break
                # print(a)
                # print(self.mode)
                if not self.keepRunning:

                    break
                try:
                    parts = [float(i) for i in line.split(" ")]

                    timestamp, temp, hum, lum = parts[0], parts[1], parts[2], parts[3]
                except AttributeError:
                    # print(f"Erreur d'accès au port série : {e}")
                    self.stop()

                except ValueError:
                    print("Erreur conversion :", line)
                    continue
                self.data = [timestamp, temp, hum, lum]
                # print(self.data)
                self.signal.emit(self.data)

            # print('d')

    def change_mode(self, m):

        self.mode = m
        print(self.mode)
        self.keepRunning = True

    def stop(self):
        self.keepRunning = False


if __name__ == "__main__":
    import sys
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    widget = MainWindow(Graph)
    widget.show()
    sys.exit(app.exec())

# class Data():

#     def __init__(self):
#         self.timestamps=[]
#         self.temp=[]
#         self.hum=[]
#         self.lum=[]
#         self.temp_high=0
#         self.hum_high=0
#         self.lum_high=0
#         self.temp_low=0
#         self.hum_low=0
#         self.lum_low=0
#         self.temp_mean=0
#         self.hum_mean=0
#         self.lum_mean=0

#     def process(self, data):
#         self.timestamps.append(data[0])
#         self.temp.append(data[1])
#         self.hum.append(data[2])
#         self.lum.append(data[3])
#         data_logger(data)
#         self.compute()

#     def highest(self):

#     def lowest(self):

#     def compute(self):

#     def display(self):


# class LivePlot:
#     def __init__(self):
#         self.app = pg.mkQApp()

#         # Fenêtre
#         self.window = QtWidgets.QWidget()
#         self.layout = QtWidgets.QVBoxLayout()
#         self.window.setLayout(self.layout)

#         # Sélecteur de signal
#         self.selector = QtWidgets.QComboBox()
#         self.selector.addItems(["Temperature", "Humidity", "Luminosity"])
#         self.layout.addWidget(self.selector)
#         #self.selector.currentTextChanged.connect(self.choice_data)
#         #self.choice = self.selector.currentText()

#         #Sélecteur de mode
#         self.modes = QtWidgets.QComboBox()
#         self.modes.addItems(["Simulation","Réél"])
#         self.layout.addWidget(self.modes)
#         #self.modes.currentTextChanged.connect(self.choice_mode)
#         #self.mode = self.modes.currentText()

#         # Graphe
#         self.plot = pg.PlotWidget(title="Données capteurs",axisItems = {'bottom': pg.DateAxisItem()})
#         self.layout.addWidget(self.plot)

#         # Label stats
#         self.stats_label = QtWidgets.QLabel("Stats:")
#         self.layout.addWidget(self.stats_label)

#         # Données
#         self.timestamps = []
#         self.temp = np.zeros(30)
#         self.hum = np.zeros(30)
#         self.lum = np.zeros(30)

#         # Courbe
#         self.curve = self.plot.plot(pen='y')

#         # Textes (créés UNE seule fois)
#         self.min_text = pg.TextItem(anchor=(0, 1))
#         self.max_text = pg.TextItem(anchor=(0, 1))
#         self.mean_text = pg.TextItem(anchor=(0, 1))

#         self.plot.addItem(self.min_text)
#         self.plot.addItem(self.max_text)
#         self.plot.addItem(self.mean_text)

#         # Labels axes
#         self.abscissa = self.plot.setLabel('bottom', 'Time')
#         self.ordinate =  self.plot.setLabel('left', "Temperature (°C)")
#         #self.ordinate.setXRange(0,35)
#         self.window.show()

#     def choice_data(self):
#         choice = self.selector.currentText()
#         return choice

#     def choice_mode(self):
#         mode = self.modes.currentText()
#         return mode

#     def update(self, timestamps, temp, hum, lum):
#         # Stockage
#         self.timestamps = np.linspace(timestamps-30, timestamps,30)

#         self.temp[-1]=temp
#         self.hum[-1]=hum
#         self.lum[-1]=lum

#         choice = self.selector.currentText()


#         if choice == "Temperature":
#             data = self.temp
#             name = "Temperature (°C)"
#             self.plot.removeItem(self.ordinate)
#             self.ordinate =  self.plot.setLabel('left', name)
#             #self.ordinate.setRange(0,35)
#             self.plot.setYRange(0,35)
#         elif choice == "Humidity":
#             data = self.hum
#             name = "Humidity (%)"
#             self.plot.removeItem(self.ordinate)
#             self.ordinate =  self.plot.setLabel('left', name)
#             #elf.ordinate.setRange(0,35)
#             self.plot.setYRange(0,100)
#         else:
#             data = self.lum
#             name = "Luminosity (%)"
#             self.plot.removeItem(self.ordinate)
#             self.ordinate =  self.plot.setLabel('left', name)
#             #self.ordinate.setRange(0,35)
#             self.plot.setYRange(0,100)
#         # Axe X
#         #x = list(range(len(data)))

#         # Update courbe
#         #print(self.timestamps)
#         print(data)
#         data[:-1] = data[1:]
#         print(data)
#         self.curve.setData(self.timestamps, data)
#         self.plot.setTitle(name)
#         #self.curve.setPos(self.timestamps[0], 0)

#         # Stats
#         # if len(data) > 0:
#         #     arr = np.array(data)
#         #     min_val = arr.min()
#         #     max_val = arr.max()
#         #     mean_val = arr.mean()

#         #     # Label texte
#         #     self.stats_label.setText(
#         #         f"{name} | Min: {min_val:.2f} | Max: {max_val:.2f} | Moy: {mean_val:.2f}"
#         #     )

#         #     # Position des textes (à droite du graphe)
#         #     xpos = len(data)

#         #     self.min_text.setText(f"Min: {min_val:.1f}")
#         #     self.min_text.setPos(xpos, min_val)

#         #     self.max_text.setText(f"Max: {max_val:.1f}")
#         #     self.max_text.setPos(xpos, max_val)

#         #     self.mean_text.setText(f"Moy: {mean_val:.1f}")
#         #     self.mean_text.setPos(xpos, mean_val)

#     def run(self):
#         pg.exec()


# class LivePlot:
#     def __init__(self):
#         self.app = pg.mkQApp()

#         self.window = QtWidgets.QWidget()
#         self.layout = QtWidgets.QVBoxLayout()
#         self.window.setLayout(self.layout)

#         self.plot = pg.PlotWidget(title="Données capteurs")
#         self.layout.addWidget(self.plot)

#         # Données
#         self.x = []
#         self.temp = []
#         self.hum = []
#         self.lum = []

#         # Courbes
#         self.curve_temp = self.plot.plot(self.temp, pen='r', name="Temp")
#         self.curve_hum = self.plot.plot(self.hum, pen='b', name="Hum")
#         self.curve_lum = self.plot.plot(self.lum, pen='g', name="Lum")

#         self.plot.addLegend()
#         self.plot.setLabel('left', 'Valeurs')
#         self.plot.setLabel('bottom', 'Mesures')

#         self.window.show()

#     def update(self, timestamp, temp, hum, lum):
#         self.x.append(len(self.x))

#         self.temp.append(temp)
#         self.hum.append(hum)
#         self.lum.append(lum)

#         self.curve_temp.setData(self.x, self.temp)
#         self.curve_hum.setData(self.x, self.hum)
#         self.curve_lum.setData(self.x, self.lum)

#     def run(self):
#         pg.exec()
