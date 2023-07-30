# iTunes-Playlist-Parser

This project is my updated and improved version of Python Playground's iTunes playlist parser

plistlib.readPlist is deprecated and this program now needs to use plistlib.load() for reading plist files.

The plotStats() function originally only worked when there was an album rating for every song in the loaded playlist. 
Now a random rating is assigned to every song that does not have a rating in order for matplotlib to draw the plots.
