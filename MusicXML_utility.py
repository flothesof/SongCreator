# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 22:33:53 2013

@author: florian
"""

import os
import zipfile 
import xml.etree.cElementTree as ET
import numpy as np

#==============================================================================
# Convenience functions
#==============================================================================
def increment_note(note, half_tones):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    ind = notes.index(note)
    return notes[(ind + half_tones) % 12]

def triplet_to_string(triplet):
    (root, alter, kind) = triplet
    if alter == False:
        return " ".join([root, kind])
    else:
        return " ".join([increment_note(root, int(alter)), kind])

def convert_chord_label_for_display(label):
    label_dict = {"major":"", "minor":"m", "dominant":"7",
                  "major-seventh":"maj7", "minor-seventh":"m7",
                  "half-diminished":"m7b5", "augmented-seventh":"7#5"}
    return label_dict[label]

def convert_chord_label_classify(label):
    label_dict = {"major":"", "minor":"m", "dominant":"",
                  "major-seventh":"", "minor-seventh":"m",
                  "half-diminished":"dim", "augmented":"+"}
    return label_dict[label]

def get_chord_from_harmony_tag(harmony_tag, transpose=0, display=True):
    """Extracts chords from a harmony tag. When necessary, this function
    can transpose by a given number of half-tones or also apply the labels
    needed for classifying chords by roots"""
    root = increment_note(harmony_tag.find('root/root-step').text, transpose)
    alter_elem = harmony_tag.find('root/root-alter')
    if alter_elem != None:
        root = increment_note(root, int(alter_elem.text))
    kind = harmony_tag.find('kind').text
    if display:
        kind = convert_chord_label_for_display(kind)                
    else:
        kind = convert_chord_label_classify(kind)
    return "".join([root, kind])
    
def get_note_from_note_tag(note_tag, transpose=0):
    """extracts note from a tag, transposing when necessary"""
    pitch = note_tag.find("pitch")
    if pitch != None: #in case the note is a rest
        note = increment_note(pitch.find("step").text, transpose)
        if pitch.find("alter") != None:
            note = increment_note(note, int(pitch.find("alter").text))
        return note
    else:
        return None

def distance_between_notes(first_note, second_note):
    """ returns distance between two notes, as a number of half-tones"""
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    first_index = notes.index(first_note)
    second_index = notes.index(second_note)
    distance = second_index - first_index
    if distance < 0:
        return distance + 12
    else:
        return distance

#==============================================================================
# Main class
#==============================================================================

class MusicXMLExtractor(object):
    def __init__(self, filename):
        """initializes a MusicXML extractor with a filename"""
        self.filename = str(filename)
        self.tree = None
        self.chord_changes = None
        self.note_chord_dict = None
        
    def read_xml_from_zip(self):
        """tries to read the MusicXML file given during initialisation and 
        creates a tree from it"""
        if os.path.exists(self.filename):
            found = True
        else:
            found = False
            raise(IOError)
        if found:
            zf = zipfile.ZipFile(self.filename, mode='r')
            namelist = zf.namelist()
            if 'musicXML.xml' in namelist:
                xml = zf.read('musicXML.xml').split('\n')
                self.tree = ET.fromstringlist(xml)
        
    def has_valid_data(self):
        """ returns True if the parsing object created from the XML exists"""
        return self.tree != None        
    
    def parse_chord_changes(self, transpose=0, display=True):
        """function that returns the chord changes in the song and their 
        frequency as a dictionary"""
        chords = []        
        for measure in self.tree.findall(".//measure"):
            for child in measure:
                if child.tag == 'harmony':
                    chords.append(
                        get_chord_from_harmony_tag(child, 
                                                   transpose=transpose,
                                                   display=display))
            
        chord_changes = {}
        for ind, val in enumerate(chords[:-1]):
            transition = "->".join([val, chords[ind + 1]])
            if transition in chord_changes:
                chord_changes[transition] += 1
            else:
                chord_changes[transition] = 1
        self.chord_changes = chord_changes                
        return chord_changes
        
        
    def parse_melody_with_harmony(self, transpose=0, display=True):
        """returns a dictionary containing note frequencies over 
        the chords appearing in the song"""
        
        def write_note_to_dict(note, current_chord, note_chord_dict):
            if not current_chord in note_chord_dict:
                note_chord_dict[current_chord] = [0] * 12
            ind = ['C', 'C#', 'D', 'D#', 'E', 'F',
                               'F#', 'G', 'G#', 'A', 'A#', 'B'].index(note)
            note_chord_dict[current_chord][ind] += 1
            
        current_chord = None
        note_chord_dict = {}
        for measure in self.tree.findall(".//measure"):
            for child in measure:
                if child.tag == 'harmony':
                    current_chord = get_chord_from_harmony_tag(child, 
                                                   transpose=transpose,
                                                   display=display)
                if child.tag == 'note':
                    note = get_note_from_note_tag(child, transpose=transpose)
                    if current_chord != None and note != None:
                        write_note_to_dict(note, current_chord, note_chord_dict)
        self.note_chord_dict = note_chord_dict
        return note_chord_dict

    def parse_song_key(self):
        """returns the major key found in the song data using the rule
        of fifths"""
        for key in self.tree.findall(".//part/measure/attributes/key"):
            fifths = int(key.find("fifths").text)
        root = 'C'
        sign = int(fifths>=0 or -1)
        for i in range(abs(fifths)):
            root = increment_note(root, 7 * sign)
        return root
    
def test_function1():
    """tests the parse_chord_changes function"""
#    filename = os.path.join(os.getcwd(), r"MusicXML_files/Keith Richards, Mick Jagger - Angie.mxl")
    filename = os.path.join(os.getcwd(), 
            r"MusicXML_files/Antonio Carlos Jobim - The Girl From Ipanema.mxl")
    m = MusicXMLExtractor(filename)
    m.read_xml_from_zip()
    print(m.parse_chord_changes())
    
def test_function2():
    """tests the parse_melody_with_harmony function"""
    filename = os.path.join(os.getcwd(), 
            r"MusicXML_files/Antonio Carlos Jobim - The Girl From Ipanema.mxl")
    m = MusicXMLExtractor(filename)
    m.read_xml_from_zip()
    print(m.parse_melody_with_harmony())

def test_function3():
    """tests the key guessing function"""
    basepath = os.path.join(os.getcwd(), "MusicXML_files")
    filenames = os.listdir(basepath)
    for filename in filter(lambda s: s.endswith(".mxl"), filenames):        
        m = MusicXMLExtractor(os.path.join(basepath, filename))
        m.read_xml_from_zip()
        root = m.parse_song_key()
        note_to_watch = increment_note(root, -3 + -1)
        note_chord_dict = m.parse_melody_with_harmony()
        note_arr = np.array([note_chord_dict[key] for key in note_chord_dict])
        total_notes = note_arr.sum()
        ind = ['C', 'C#', 'D', 'D#', 'E', 'F',
                       'F#', 'G', 'G#', 'A', 'A#', 'B'].index(note_to_watch)
        note_to_watch_count = note_arr[:, ind].sum()
        print(filename, root, note_to_watch_count, total_notes)
        print("%.2f" % (note_to_watch_count / float(total_notes) * 100))
    
def test_function4():
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
    
    basepath = os.path.join(os.getcwd(), "MusicXML_files")
    filenames = os.listdir(basepath)
    # loop over files in folder
    for filename in filter(lambda s: s.endswith(".mxl"), filenames):        
        print(filename)
        m = MusicXMLExtractor(os.path.join(
                                                    basepath, filename))
        m.read_xml_from_zip()
        root = m.parse_song_key()
        distance_to_C_scale = distance_between_notes(
                                                                root, 'C')
        chord_changes = m.parse_chord_changes(transpose=distance_to_C_scale,
                              display=False)
        for item in chord_changes.keys():
            chord1, chord2 = item.split("->")
            chord_transition_matrix[all_chords.index(chord1), 
                                    all_chords.index(chord2)] += chord_changes[item]
                                    
        note_chord_dict = m.parse_melody_with_harmony(transpose=distance_to_C_scale,
                                                              display=False)        
    # do some plotting
    return chord_transition_matrix
        
if __name__ == "__main__":
#    test_function1()                        
#    test_function2()                        
#    test_function3()                        
    ctm = test_function4()                        
    