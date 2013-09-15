# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 22:33:53 2013

@author: florian
"""

import os
import zipfile 
import xml.etree.cElementTree as ET

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

#==============================================================================
# Main class
#==============================================================================

class MusicXMLExtractor(object):
    def __init__(self, filename):
        self.filename = str(filename)
        self.xml = None
        
    def read_xml_from_zip(self):
        if os.path.exists(self.filename):
            found = True
        else:
            found = False
            raise(IOError)
        if found:
            zf = zipfile.ZipFile(self.filename, mode='r')
            namelist = zf.namelist()
            if 'musicXML.xml' in namelist:
                self.xml = zf.read('musicXML.xml').split('\n')
        
    def has_valid_xml(self):
        return self.xml != None        

    def parse_chords(self):
        tree = ET.fromstringlist(self.xml)
        chords = []
        for elem in tree.findall('.//harmony'):
            root = elem.find('root/root-step').text
            alter_elem = elem.find('root/root-alter')
            alter = (alter_elem != None and alter_elem.text)
            kind = elem.find('kind').text
            chords.append((root, alter, kind))
        return map(triplet_to_string, chords)
    

    def calc_chord_changes(self):
        chords = self.parse_chords()
        chord_changes = {}
        for ind, val in enumerate(chords[:-1]):
            transition = "->".join([val, chords[ind + 1]])
            if transition in chord_changes:
                chord_changes[transition] += 1
            else:
                chord_changes[transition] = 1
        return chord_changes
        
if __name__ == "__main__":
    filename = '/home/florian/workspace/SongCreator/MusicXML_files/Keith Richards, Mick Jagger - Angie.mxl'
    m = MusicXMLExtractor(filename)
    m.read_xml_from_zip()