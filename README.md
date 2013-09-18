SongCreator
===========

This is a machine learning based song creator. It follows the core principles of the Microsoft Research edited [Songsmith](http://research.microsoft.com/en-us/um/redmond/projects/songsmith/) (ex [Mysong](http://research.microsoft.com/en-us/um/people/dan/mysong)) software.
In this first stage, it can produce some graphical output based on a MusicXML file:

- frequency display for all chord transitions present in the file
- frequency display of the twelve chromatic notes over the chords that appear in the song

Usage
=====

Click the *Open .mxml file* to load a MusicXML file. The two tabs are then updated according to the data from the file.

- The *Chord analysis tab* displays a bar plot with the chord transitions that appear in the tune and their frequency ![Screenshot](/Screenshots/2013_09_16_chords.png)
- the *Melody analysis tab* displays a matrix with each row being the frequency of the twelve chromatic notes played over each chord in the song ![Screenshot](/Screenshots/2013_09_16_melody.png)

Bibliography
============
1. D. Morris, I. Simon, and S. Basu, "Exposing Parameters of a Trained Dynamic Model for Interactive Music Creation.," in AAAI, 2008, pp. 784–791.
2. I. Simon, D. Morris, and S. Basu, "MySong: automatic accompaniment generation for vocal melodies," in Proceedings of the SIGCHI Conference on Human Factors in Computing Systems, 2008, pp. 725–734.

Links
=====

- [Snippet for integrating Matplotlib widget into a PyQt4 application](http://stackoverflow.com/questions/12459811/how-to-embed-matplotib-in-pyqt-for-dummies)
- [Snippet for sorting a dict by values](http://stackoverflow.com/questions/613183/python-sort-a-dictionary-by-value)