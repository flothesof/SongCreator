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
            if 'text' in elem.find('kind').attrib:
                kind_attrib = elem.find('kind').attrib['text']
                chords.append((root, alter, kind_attrib))
            else:
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
        
        
    def parse_melody_with_harmony(self):
        def get_chord_from_harmony_tag(harmony_tag):
            root = harmony_tag.find('root/root-step').text
            alter_elem = harmony_tag.find('root/root-alter')
            if alter_elem != None:
                root = increment_note(root, int(alter_elem.text))
            if 'text' in harmony_tag.find('kind').attrib:
                kind_attrib = harmony_tag.find('kind').attrib['text']
                return " ".join([root, kind_attrib])
            else:
                kind = harmony_tag.find('kind').text                
                return " ".join([root, kind])
            
        def get_note_from_note_tag(note_tag):
            pitch = note_tag.find("pitch")
            if pitch != None: #in case the note is a rest
                note = pitch.find("step").text
                if pitch.find("alter") != None:
                    note = increment_note(note, int(pitch.find("alter").text))
                return note
            else:
                return None
        
        def write_note_to_dict(note, current_chord, note_chord_dict):
            if not current_chord in note_chord_dict:
                note_chord_dict[current_chord] = [0] * 12
            ind = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'].index(note)
            note_chord_dict[current_chord][ind] += 1
            
        current_chord = None
        note_chord_dict = {}
        tree = ET.fromstringlist(self.xml)
        for measure in tree.findall(".//measure"):
            for child in measure:
                if child.tag == 'harmony':
                    current_chord = get_chord_from_harmony_tag(child)
                if child.tag == 'note':
                    note = get_note_from_note_tag(child)
                    if current_chord != None and note != None:
                        write_note_to_dict(note, current_chord, note_chord_dict)
                        
        return note_chord_dict
                        
if __name__ == "__main__":
    filename = os.path.join(os.getcwd(), r"MusicXML_files/Antonio Carlos Jobim - The Girl From Ipanema.mxl")
#    filename = os.path.join(os.getcwd(), r"MusicXML_files/Keith Richards, Mick Jagger - Angie.mxl")
    m = MusicXMLExtractor(filename)
    m.read_xml_from_zip()
    print m.calc_chord_changes()
    print m.parse_chords()