import plistlib
from matplotlib import pyplot
import numpy as np
import sys
import re, argparse
import random

def findDuplicates(fileName):
     """This function searches for duplicate tracks in an iTunes playlist."""
     print('Finding duplicate tracks in %s...' % fileName)
     with open(fileName, 'rb') as file:
        plist = plistlib.load(file)         # Read in the playlist file
     tracks = plist['Tracks']               # Access the tracks dictionary in the playlist XML file
     trackNames = {}                        # Dictionary to store duplicate tracks

     for trackID, track in tracks.items():
        try:
            name = track['Name']
            duration = track['Total Time']

            # Check if the names match and if the rounded down durations match. 
            # Floor divide by 1000 to round to the nearest second since Apple stores duration as miliseconds
            if name in trackNames and duration//1000 == trackNames[name][0]//1000:
                count = trackNames[name][1]
                trackNames[name] = (duration, count + 1)    # trackNames is a dictionary in which the value is a pair 
                                                            # containing the track's duration and the number of appearances that track has
            else:
                trackNames[name] = (duration, 1)

        except:
            pass
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
    """This function attempts to find common tracks across multiple different iTunes playlists."""
    trackNameSets = []
    for fileName in fileNames:
        trackNames = set()          # Create a set for each playlist in order to compare them through set intersection
        with open(fileName, 'rb') as file:
            plist = plistlib.load(file)
        tracks = plist['Tracks']
        for trackID, track in tracks.items():
            try: 
                trackNames.add((track['Name'], track['Total Time']//1000))    # Add the track in as a pair of name, duration
            except:
                pass
        trackNameSets.append(trackNames)
    commonTracks = set.intersection(*trackNameSets) # Intersect the two sets to find the common tracks matched by name and duration
    if len(commonTracks) > 0:
        file = open("comon.txt", 'w')
        for value in commonTracks:
            file.write("%s\n" % str(value))   # Use encode to ensure that unicode characters are saved
        file.close()
        print("%d common tracks found. Track names written to common.txt" % len(commonTracks))
    else:
        print("No common tracks.")

def plotStats(fileName):
    """This function plots creates a scatter plot, histogram, and a bar chart of statistics for a given playlist."""
    with open(fileName, 'rb') as file:
        plist = plistlib.load(file)
    tracks = plist['Tracks']
    ratings = []
    durations = []

    # Loop through the tracks dictionary and add ratings to ratings list and durations to durations list
    for trackID, track in tracks.items():
        durations.append(track['Total Time'])
        # ratings.append(track['Album Rating'])     appending the actual album rating only works if there is a rating for every single 
        #                                           song in the playlist, so for the sake of experimentation we will fabricate random album ratings
        ratings.append(random.randint(0, 100))

    if ratings == [] or durations == []:
        print("No valid album rating or total time data in %s." % fileName)
        return

    x = (np.array(durations, np.int32)) / 60000.0   # Divide by 60000.0 to convert miliseconds to seconds
    y = np.array(ratings, np.int32)

    # Create scatterplot
    pyplot.subplot(2, 1, 1)
    pyplot.plot(x, y, 'o')
    pyplot.axis([0, 1.05 * np.max(x), -1, 110]) # This alters the x and y axis to give the scatter plot some padding
    pyplot.xlabel('Track Duration')
    pyplot.ylabel('Count')

    # Create histogram
    pyplot.subplot(2, 1, 2)
    pyplot.hist(x, bins=20)
    pyplot.xlabel('Track Duration')
    pyplot.ylabel('Count')

    # Create Bar Chart


    pyplot.show()


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
