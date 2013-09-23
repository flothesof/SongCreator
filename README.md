SongCreator
===========

This is a machine learning based song creator. It follows the principles of the Microsoft Research edited [Songsmith](http://research.microsoft.com/en-us/um/redmond/projects/songsmith/) (ex [Mysong](http://research.microsoft.com/en-us/um/people/dan/mysong)) software, as exposed in [1] and [2].
In this first stage, it can do two things:

- produce some graphical output based on a MusicXML file
	- frequency display for all chord transitions present in the file
	- frequency display of the twelve chromatic notes over the chords that appear in the song
	
- produce some graphical output based on a folder containing MusicXML files


Usage
=====

Click the *Open .mxml file* to load a MusicXML file. The two tabs are then updated according to the data from the file.

- The *Chord analysis tab* displays a bar plot with the chord transitions that appear in the tune and their frequency ![Screenshot](/Screenshots/2013_09_23_chords.png)
- the *Melody analysis tab* displays a matrix with each row being the frequency of the twelve chromatic notes played over each chord in the song ![Screenshot](/Screenshots/2013_09_23_melody.png)

Note: when clicking the *transpose to C* button, you'll see the equivalent chords and melody matrices if the song was played in C major. ![Screenshot](/Screenshots/2013_09_23_chords_transposed.png)

Open the *Folder analysis* tab and click on the button *Open folder containing .mxml files* to parse all MusicXML files in a directory. Two matrices will be displayed in the graphical view. ![Screenshot](/Screenshots/2013_09_23_folder.png)

- On the left, you'll see the chord transition matrix, indexed by chord root. The five rows underneath each root correspond to major, minor, augmented, diminished and suspended chord types.
- On the right, you'll see the melody observation matrix, indexed by chord root in rows and note in columns. This gives the probability of playing a given note over a given chord in the melody.

Bibliography
============
1. D. Morris, I. Simon, and S. Basu, "Exposing Parameters of a Trained Dynamic Model for Interactive Music Creation.," in AAAI, 2008, pp. 784–791.
2. I. Simon, D. Morris, and S. Basu, "MySong: automatic accompaniment generation for vocal melodies," in Proceedings of the SIGCHI Conference on Human Factors in Computing Systems, 2008, pp. 725–734.

Links
=====

- [Snippet for integrating Matplotlib widget into a PyQt4 application](http://stackoverflow.com/questions/12459811/how-to-embed-matplotib-in-pyqt-for-dummies)
- [Snippet for sorting a dict by values](http://stackoverflow.com/questions/613183/python-sort-a-dictionary-by-value)