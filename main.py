# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 20:22:22 2026

@author: Majdo
"""

# if __name__ == '__main__':
#     from realtime_plot import MainWindow,Graph,Worker
#     import sys
#     from PySide6.QtWidgets import QApplication

#     if not QApplication.instance():
#         app = QApplication(sys.argv)
#     else:
#         app = QApplication.instance()

#     widget = MainWindow(Graph)
#     widget.show()
#     #worker = Worker()
#     #widget.make_connection(worker)
#    # worker.start()
#     sys.exit(app.exec())
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


# from serial_reader import read_serial
# from data_logger import save_data
# from datetime import datetime
# from PyQt5 import QtWidgets, QtCore
# import time
# import sys
# plot = LivePlot()


# for line in read_serial(mode='sim'):
#     parts = [float(i) for i in line.split(' ')]

#     if len(parts) != 3:
#         print("Format incorrect :", line)
#         continue
#     try:
#         timestamps = time.time()
#         temp, hum, lum = parts[0],parts[1],parts[2]#map(float, parts[6:])
#     except ValueError:
#         print("Erreur conversion :", line)
#         continue
#     print(timestamps, temp, hum, lum)
#    # try:
#    #     save_data('ello', timestamp, temp, hum, lum)
#     #except Exception as e:
#      #  print("Erreur sauvegarde :", e)
#     try:
#         plot.update(timestamps, temp, hum, lum)
#         QtWidgets.QApplication.processEvents()  # IMPORTANT
#     except Exception as e:
#         print("Erreur graphique :", e)
# for line in read_serial(mode="real"):
#     print("RAW:", line)  # debug

#     parts = line.split('\t')

#     if len(parts) != 9:
#         print("Format incorrect :", line)
#         continue

#     try:
#         jour, mois, annee, heure, minute, seconde = map(int, parts[:6])
#         temp, hum, lum = map(float, parts[6:])

#         timestamp = datetime(2000 + annee, mois, jour, heure, minute, seconde)

#     except ValueError:
#         print("Erreur conversion :", line)
#         continue

#     print(timestamp, temp, hum, lum)

#     try:
#         save_data('ello', timestamp, temp, hum, lum)

#     except Exception as e:
#         print("Erreur sauvegarde :", e)

#     try:
#         plot.update(timestamp, temp, hum, lum)
#         QtWidgets.QApplication.processEvents()  # IMPORTANT
#     except Exception as e:
#         print("Erreur graphique :", e)

#
# plot.run()

    # parts = line.split(',')

    # if len(parts) != 3:
    #     print("Format incorrect :", line)
    #     continue

    # try:
    #     temp, hum, lum = map(float, parts)
    # except ValueError:
    #     print("Erreur conversion :", line)
    #     continue

    # print(temp, hum, lum)

    # try:
    #     save_data('data/data.csv', temp, hum, lum)
    # except Exception as e:
    #     print("Erreur sauvegarde :", e)
# dans ta boucle :
