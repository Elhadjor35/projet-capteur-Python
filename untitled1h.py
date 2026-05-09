#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  9 18:03:01 2026

@author: elhadj
"""
from PySide6.QtWidgets import QApplication, QVBoxLayout, QComboBox, QLabel, QFileDialog
from PySide6.QtCore import QThread, Signal, Slot
import pyqtgraph as pg
import numpy as np
import time
import pandas as pd
file = QFileDialog.getOpenFileName(
    # '28030254.TXT'
)
print(file[0])
