# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 07:11:18 2026

@author: Majdo
"""

import pyqtgraph as pg
import pandas as pd
from PyQt5 import QtWidgets

# =========================
# Lecture du fichier
# =========================
df = pd.read_table(
    '28030254.TXT',
    sep='\s+',
    names=['Jour', 'Mois', 'Année', 'Heure',
           'Minute', 'Seconde', 'Temp', 'Hum', 'Lum'],
    header=0,
    parse_dates={'Time': ['Jour', 'Mois',
                          'Année', 'Heure', 'Minute', 'Seconde']},
    date_format='%d %m %y %H %M %S'
)

# Nettoyage
df = df.drop(df[(df["Temp"] == 0) & (df["Lum"] == 0) &
             (df["Hum"] == 0)].index).reset_index(drop=True)

df['Time'] = df['Time'].dt.tz_localize('Europe/Paris')
df['Time_unix'] = df['Time'].astype(int) / 10**9

# =========================
# Application Qt
# =========================
app = pg.mkQApp()

# Fenêtre principale
window = QtWidgets.QWidget()
window.setWindowTitle("Capteurs interactif")
window.resize(1200, 600)

# Layout horizontal
layout = QtWidgets.QHBoxLayout()
window.setLayout(layout)

# =========================
# Liste à gauche
# =========================
list_widget = QtWidgets.QListWidget()
list_widget.addItems(["Température", "Humidité", "Luminosité"])
layout.addWidget(list_widget, 1)

# =========================
# Zone graphique à droite
# =========================
plot_widget = pg.PlotWidget(axisItems={'bottom': pg.DateAxisItem()})
plot_widget.showGrid(x=True, y=True)
layout.addWidget(plot_widget, 4)

# =========================
# Fonction affichage
# =========================


def update_plot():
    plot_widget.clear()

    choix = list_widget.currentItem().text()

    if choix == "Température":
        y = df['Temp']
        couleur = 'y'
        titre = "Température (°C)"

    elif choix == "Humidité":
        y = df['Hum']
        couleur = 'c'
        titre = "Humidité (%)"

    elif choix == "Luminosité":
        y = df['Lum']
        couleur = 'm'
        titre = "Luminosité (%)"

    x = df['Time_unix']

    # Courbe
    plot_widget.plot(x, y, pen=couleur)
    plot_widget.setTitle(titre)

    # Stats
    y_min = y.min()
    y_max = y.max()
    y_mean = y.mean()

    # Texte
    text = pg.TextItem(
        text=f"Min: {y_min}\nMax: {y_max}\nMoy: {y_mean:.2f}",
        color='w'
    )
    plot_widget.addItem(text)
    text.setPos(x.iloc[0], y_max)

    # Ligne moyenne
    plot_widget.addLine(y=y_mean, pen='r')


# =========================
# Connexion clic
# =========================
list_widget.currentItemChanged.connect(update_plot)

# Sélection par défaut
list_widget.setCurrentRow(0)

# =========================
# Lancement
# =========================
window.show()

if __name__ == '__main__':
    pg.exec()
