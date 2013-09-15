# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 20:06:40 2013

@author: florian
"""
import sys
from PyQt4 import QtGui, uic
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt
import random
import os
import numpy as np

import MusicXML_utility

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        # load the UI from the disk
        self.ui = uic.loadUi("SongCreator.ui", self)

        # customize the UI
        self.initUI()
        
        # init class data
        self.initData()       
        
        # connect slots
        self.connectSlots()
        
    def initUI(self):
        self.figure = plt.figure(facecolor='white')

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)        

        layout = self.ui.tab.layout()   
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
    def initData(self):
        pass
        
    def connectSlots(self):
        self.ui.pushButton.clicked.connect(self.openMusicXMLFile)
    
    def plot(self):
        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(10)]

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.hold(False)

        # plot data
        ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()
        
    def plot_chord_changes(self, chord_changes):
        occurences = [chord_changes[key] for key in chord_changes]
        ax = self.figure.add_subplot(111)
        ax.hold(False)
        ax.bar(np.arange(len(occurences)), occurences)
        plt.xticks(0.5 + np.arange(len(occurences)))
        locs, labels = plt.xticks()
        plt.xticks(locs, chord_changes.keys(), rotation = 90)
        
        # refresh canvas
        self.canvas.draw()

    def openMusicXMLFile(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
                '/home')
        self.ui.lineEdit.setText(fname)
        self.mxml_extractor = MusicXML_utility.MusicXMLExtractor(fname)
        self.mxml_extractor.read_xml_from_zip()
        if self.mxml_extractor.has_valid_xml():
            chord_changes = self.mxml_extractor.calc_chord_changes()
            self.plot_chord_changes(chord_changes)
            


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())