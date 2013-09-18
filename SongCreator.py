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
import os
import numpy as np

import MusicXML_utility

class MplFigure(object):
    def __init__(self, parent):
        self.figure = plt.figure(facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, parent)

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
        # chord tab
        self.chord_ui = MplFigure(self)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.chord_ui.toolbar)
        layout.addWidget(self.chord_ui.canvas)
        self.ui.tab.setLayout(layout)
        
        # melody tab
        self.melody_ui = MplFigure(self)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.melody_ui.toolbar)
        layout.addWidget(self.melody_ui.canvas)
        self.ui.tab_2.setLayout(layout)
        
    def initData(self):
        pass
        
    def connectSlots(self):
        self.ui.pushButton.clicked.connect(self.openMusicXMLFile)
        
    def plot_chord_changes(self, chord_changes):
        occurences = [chord_changes[key] for key in chord_changes]
        plt.figure(self.chord_ui.figure.number)
        plt.clf()
        ax = self.chord_ui.figure.add_subplot(111)
        ax.bar(np.arange(len(occurences)), occurences)
        plt.xticks(0.5 + np.arange(len(occurences)))
        locs, labels = plt.xticks()
        plt.xticks(locs, chord_changes.keys(), rotation = 90)
        plt.tight_layout()
        
        # refresh canvas
        self.chord_ui.canvas.draw()

    def plot_melody_matrix(self, note_chord_dict):
        plt.figure(self.melody_ui.figure.number)
        plt.clf()        
        self.melody_ui.figure.add_subplot(111)
        note_arr = np.array([note_chord_dict[key] for key in note_chord_dict])
        plt.matshow(note_arr, fignum=False, cmap=plt.cm.cool)
        plt.xticks(np.arange(0, 12), ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']);
        plt.yticks(np.arange(0, len(note_chord_dict.keys())), note_chord_dict.keys());
        plt.colorbar(shrink=0.75)
        plt.tight_layout()
        
        # refresh canvas
        self.melody_ui.canvas.draw()

    def openMusicXMLFile(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
                os.getcwd())
        self.ui.lineEdit.setText(fname)
        self.mxml_extractor = MusicXML_utility.MusicXMLExtractor(fname)
        self.mxml_extractor.read_xml_from_zip()
        if self.mxml_extractor.has_valid_data():
            chord_changes = self.mxml_extractor.parse_chord_changes()
            self.plot_chord_changes(chord_changes)
            note_chord_dict = self.mxml_extractor.parse_melody_with_harmony()
            self.plot_melody_matrix(note_chord_dict)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())