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

        # folder analysis tab
        self.folder_ui = MplFigure(self)
        layout = self.ui.tab_3.layout()
        layout.addWidget(self.folder_ui.toolbar)        
        layout.addWidget(self.folder_ui.canvas)
        
    def initData(self):
        pass
        
    def connectSlots(self):
        self.ui.pushButton.clicked.connect(self.openMusicXMLFile)
        self.ui.pushButton_2.clicked.connect(self.analyzeFolder)
        self.ui.checkBox.toggled.connect(self.toggle_transposition)        
        
    def plot_chord_changes(self, chord_changes):
        sorted_occurences = [(key, chord_changes[key]) for key in sorted(
                                        chord_changes, key=chord_changes.get)]
        occurences = [item[1] for item in sorted_occurences]
        new_labels = [item[0] for item in sorted_occurences]
        plt.figure(self.chord_ui.figure.number)
        plt.clf()
        ax = self.chord_ui.figure.add_subplot(111)
        ax.bar(np.arange(len(occurences)), occurences)
        plt.xticks(0.5 + np.arange(len(occurences)))
        locs, labels = plt.xticks()
        plt.xticks(locs, new_labels, rotation = 90)
        plt.tight_layout()
        self.chord_ui.canvas.draw() # refresh canvas

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
        self.melody_ui.canvas.draw() # refresh canvas

    def toggle_transposition(self, toggle):
        try:
            valid_data = self.mxml_extractor.has_valid_data()
        except AttributeError:
            return
        if valid_data:
            if toggle:
                root = self.mxml_extractor.parse_song_key()
                transpose_distance = MusicXML_utility.distance_between_notes(
                                                                    root,
                                                                    'C')
            else:
                transpose_distance = 0
            chord_changes = self.mxml_extractor.parse_chord_changes(
                                                transpose=transpose_distance)
            self.plot_chord_changes(chord_changes)
            note_chord_dict = self.mxml_extractor.parse_melody_with_harmony(
                                                transpose=transpose_distance)
            self.plot_melody_matrix(note_chord_dict)

    def openMusicXMLFile(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
                os.getcwd())
        self.ui.lineEdit.setText(fname)
        self.mxml_extractor = MusicXML_utility.MusicXMLExtractor(fname)
        self.mxml_extractor.read_xml_from_zip()
        if self.mxml_extractor.has_valid_data():
            # GUI modification
            self.ui.checkBox.setChecked(False)
            root = self.mxml_extractor.parse_song_key()
            minor_root = MusicXML_utility.increment_note(root, -3) + "m"
            self.ui.lineEdit_2.setText(" / ".join([root, minor_root]))
            # song parsing
            chord_changes = self.mxml_extractor.parse_chord_changes()
            self.plot_chord_changes(chord_changes)
            note_chord_dict = self.mxml_extractor.parse_melody_with_harmony()
            self.plot_melody_matrix(note_chord_dict)

    def analyzeFolder(self):
        folder_name = QtGui.QFileDialog.getExistingDirectory(self, 
             'Select directory', os.getcwd(), QtGui.QFileDialog.ShowDirsOnly)
        folder_name = str(folder_name)
        
        filenames = map(str, os.listdir(folder_name))
        
        # initialize global chord index
        all_chords = []
        chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F',
                                   'F#', 'G', 'G#', 'A', 'A#', 'B']
        for note in chromatic_scale:
            for triad in ['', 'm', '+', 'dim', 'sus']:
                all_chords.append("".join([note, triad]))
        
        # initialize chord transition matrix        
        chord_transition_matrix = np.zeros((60, 60))
        # initialize melody observation matrix
        melody_observation_matrix = np.zeros((60, 12))

        # loop over files in folder
        for filename in filter(lambda s: s.endswith(".mxl"), filenames):        
            print filename
            m = MusicXML_utility.MusicXMLExtractor(
                                    os.path.join(folder_name, filename))
            m.read_xml_from_zip()
            root = m.parse_song_key()
            distance_to_C_scale = MusicXML_utility.distance_between_notes(
                                                                    root,
                                                                    'C')
            # parse chord transitions                                                         
            chord_changes = m.parse_chord_changes(
                                                transpose=distance_to_C_scale,
                                                display=False)
            temporary_chord_changes = np.zeros((60, 60))                                    
            for item in chord_changes.keys():
                chord1, chord2 = item.split("->")
                change = chord_changes[item] 
                temporary_chord_changes[all_chords.index(chord1), 
                                        all_chords.index(chord2)] += change
            
                        
            s = temporary_chord_changes.sum(axis=1)
            indices = (s != 0)
            temporary_chord_changes[indices, :] = (temporary_chord_changes[indices, :].T / s[indices]).T
            chord_transition_matrix += temporary_chord_changes
            
            # parse melody                 
            note_chord_dict = m.parse_melody_with_harmony(
                                                transpose=distance_to_C_scale,
                                                display=False)        
            for chord in note_chord_dict.keys():
                row = np.array(note_chord_dict[chord], dtype=np.float32)
                if row.sum() != 0:
                    row /= row.sum()
                melody_observation_matrix[all_chords.index(chord), :] += row

        # normalize chord transition matrix so each row sums to 1
        s = chord_transition_matrix.sum(axis=1)
        indices = (s != 0)
        chord_transition_matrix[indices, :] = (chord_transition_matrix[indices, :].T / s[indices]).T
        
        # plot chord transition matrix
        plt.figure(self.folder_ui.figure.number)
        plt.clf()        
        self.folder_ui.figure.add_subplot(121)
        plt.matshow(chord_transition_matrix, fignum=False, cmap=plt.cm.cool)
        plt.colorbar(shrink=0.75)
        plt.xticks(5 * np.arange(12), chromatic_scale)        
        plt.yticks(5 * np.arange(12), chromatic_scale)        
        plt.grid(True)
        plt.title("Chord transition matrix")
        
        # plot melody observation matrix
        self.folder_ui.figure.add_subplot(122)
        plt.matshow(melody_observation_matrix, fignum=False, 
                    cmap=plt.cm.cool, aspect=0.2)
        plt.colorbar(shrink=0.75)
        plt.xticks(np.arange(12), chromatic_scale)        
        plt.yticks(5 * np.arange(12), chromatic_scale)        
        plt.title("Melody observation matrix")
        
        # refresh window        
        plt.tight_layout()
        self.folder_ui.canvas.draw() # refresh canvas
                                        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())