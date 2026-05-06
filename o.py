#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 19:20:37 2026

@author: elhadj
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 14:58:56 2026

@author: elhadj
"""
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

pg.mkQApp()

# Axis
a2 = pg.AxisItem("left")
a3 = pg.AxisItem("left")


# ViewBoxes
v2 = pg.ViewBox()
v3 = pg.ViewBox()


# main view
pw = pg.GraphicsView()
pw.setWindowTitle('pyqtgraph example: multiple y-axis')
pw.show()

# layout
l = pg.GraphicsLayout()
pw.setCentralWidget(l)

# add axis to layout
# watch the col parameter here for the position
l.addItem(a2, row=1, col=5, rowspan=1, colspan=1)
l.addItem(a3, row=1, col=4, rowspan=1, colspan=1)


# Blank axis used for aligning things
ax = pg.AxisItem(orientation='bottom')
ax.setPen('#000000')
pos = (2, 2)
l.addItem(ax, *pos)

# plotitem and viewbox
# at least one plotitem is used whioch holds its own viewbox and left axis
pI = pg.PlotItem()
v1 = pI.vb  # reference to viewbox of the plotitem
l.addItem(pI, row=1, col=8, rowspan=2, colspan=1)  # add plotitem to layout

# split off 1st axis and put to side
pI.axis_left = pI.getAxis('left')
pos = (1, 7)
l.addItem(pI.axis_left, *pos)

# add viewboxes to layout
l.scene().addItem(v2)
l.scene().addItem(v3)


# link axis with viewboxes
a2.linkToView(v2)
a3.linkToView(v3)


# link viewboxes
v2.setXLink(v1)
v3.setXLink(v2)

# axes labels
pI.getAxis("left").setLabel('axis 1 in ViewBox of PlotItem', color='#FFFFFF')
a2.setLabel('axis 2 in Viewbox 2', color='#2E2EFE')
a3.setLabel('axis 3 in Viewbox 3', color='#2EFEF7')


# slot: update view when resized
def updateViews():
    v2.setGeometry(v1.sceneBoundingRect())
    v3.setGeometry(v1.sceneBoundingRect())


# data
x = [1, 2, 3, 4, 5, 6]
y1 = [0, 4, 6, 8, 10, 4]
y2 = [0, 5, 7, 9, 11, 3]
y3 = [0, 1, 2, 3, 4, 12]


# plot
v1.addItem(pg.PlotCurveItem(x, y1, pen='#FFFFFF'))
v2.addItem(pg.PlotCurveItem(x, y2, pen='#2E2EFE'))
v3.addItem(pg.PlotCurveItem(x, y3, pen='#2EFEF7'))


# updates when resized
v1.sigResized.connect(updateViews)

# autorange once to fit views at start
v2.enableAutoRange(axis=pg.ViewBox.XYAxes, enable=True)
v3.enableAutoRange(axis=pg.ViewBox.XYAxes, enable=True)

updateViews()

if __name__ == '__main__':
    pg.exec()
