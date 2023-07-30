import plistlib
from matplotlib import pyplot
import numpy as np
import sys
import re, argparse

def findDuplicates(fileName):
     """This function searches for duplicate tracks in an iTunes playlist."""
     print('Finding duplicate tracks in %s...' % fileName)
     plist = plistlib.readPlist(fileName)   # Read in the playlist file
     tracks = plist['Tracks']               # Access the tracks dictionary in the playlist XML file
     trackNames = {}                        # Dictionary to store duplicate tracks

     for trackID, track in tracks.items():
        try:
            name = track['Name']
            duration = track['Duration']

            # Check if the names match and if the rounded down durations match. 
            # Floor divide by 1000 to round to the nearest second since Apple stores duration as miliseconds
            if name in trackNames and duration//1000 == trackNames[name][0]//1000:
                count = trackNames[name][1]
                trackNames[name] = (duration, count + 1)    # trackNames is a dictionary in which the value is a pair 
                                                            # containing the track's duration and the number of appearances that track has
            else:
                trackNames[name] = (duration, 1)

        except error as e:
            print(e)
        duplicates = []
        for key, value in trackNames.items():
            # Check if the count is greater than 1
            if value[1] > 1:
                duplicates.append((value[1], key))      # Save the count and the name of the track 

        if len(duplicates) > 0:
            print("Found % d duplicates. Track names saved to duplicates.txt" % len(dups))
        else:
            print("No duplicates found.")

        file = open("duplicates.txt", 'w')
        for value in duplicates:
            file.write("[%d] %s\n" % (val[0], val[1]))  # Write the count and the name of the track
        file.close()

def findCommonTracks(fileNames):
    pass


if __name__ == '__main__':
    description = """This program parses iTunes playlist files as exported in .xml format."""

    parser = argparse.ArgumentParser(description=description)   # Create the parser and a group which limits the command line arguments to 1
    group = parser.add_mutually_exclusive_group()

    group.add_argument('--common', nargs='*', dest='plFiles', required=False)
    group.add_argument('--stats', dest='plFile', required=False)
    group.add_argument('--duplicates', dest='plFileD', required=False)

    args = parser.parse_args()

    if args.plFiles:
        findCommonTracks(args.plFiles)
    elif args.plFile:
        plotStats(args.plFile)
    elif args.plFileD:
        findDuplicates(args.plFileD)
    else:
        print("These are not the tracks you are looking for.")
