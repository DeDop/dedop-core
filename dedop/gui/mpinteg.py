"""
Experimental code demonstrating how to integrate matplotlib with PyQt5.
See http://stackoverflow.com/questions/12459811/how-to-embed-matplotib-in-pyqt-for-dummies.
"""

import random

import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class Window(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.setWindowTitle('matplotlib Integration Example')

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.pushButton = QtWidgets.QPushButton('Plot')
        self.pushButton.clicked.connect(self.plot)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.pushButton)
        self.setLayout(layout)

    def plot(self):
        # random data
        data = [random.gauss(0.0, 3.0) for i in range(100)]
        # create an axis
        ax = self.figure.add_subplot(111)
        # discards the old graph
        ax.hold(False)
        # plot data
        ax.plot(data, '*-')
        # refresh canvas
        self.canvas.draw()
