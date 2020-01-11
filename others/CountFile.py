import os
import csv

# Take path of directry containing audio data.
path = './../audio'  
# Take directry names in audio.
# Almost of these names is name of instrument.
dirs = os.listdir(path)
# This is an array that will have directry name and number of files.
numberOfEachDirectry = []

# Add each directry name and number of files for that directry.
for directry in dirs:
    dirPath = './../audio/%s' % directry
    files = os.listdir(dirPath)
    count = len(files)
    numberOfEachDirectry.append([directry, count])
    
# Sort about directry name.
numberOfEachDirectry.sort()

with open('./../csv_files/NumberOfFilesForEachDirectries.csv', 'w') as fileCount:
    writer = csv.writer(fileCount)
    writer.writerow(['Directry name', 'Number of files'])
    for row in numberOfEachDirectry:
        writer.writerow(row)
