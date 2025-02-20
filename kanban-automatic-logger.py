import csv
import os

# Make sure the directory below has no "\" and instead only has "/"
mainFolderToLogDir = "" # Insert the file path of the folder you want to "copy"
outputDir = "generated" # This is the output folder which is where the .csv file will be placed.

# Base Data to hold every file as their name, stage will always be Generated, parent folder name, no note by default.
data = [["File Name", "File Type", "Stage", "Parent Folder", "Changes / Notes"]]

# This array holds the file paths to scan folders for recursion.
scanFolders = [mainFolderToLogDir]

# Function scans all of the files in a directory/folder. If it's a file, it will insert it into the data. 
# If it's a folder, it is marked to be scanned again.
# After scanning the whole folder, for every new folder that was scanned, it will scan those too. 
# This is known as recursion.
folderCount = 0
trueFoundFiles = 0
def scanFolder(folderFilePath: str):
    global trueFoundFiles
    global folderCount
    folderCount += 1

    print("[kanban-automatic-logger] Scanning " + folderFilePath)
    scanFolders.remove(folderFilePath) # Remove the folder from the Array to not repeatedly scan it.

    needToScanAgain = False # Do not scan again if there are no folders a.k.a a break statement.
    foundFiles = 0
    for file in os.listdir(os.fsencode(folderFilePath)):
        filename = os.fsdecode(file)
        filePath = folderFilePath + "/" + filename
        realFile = os.fsencode(filePath)

        if os.path.isdir(realFile):
            # File is a folder/directory
            scanFolders.append(filePath)
            needToScanAgain = True
        else:
            # File is not a folder/directory.
            fileNameSplit = filename.split(".")
            fileExtension = fileNameSplit[len(fileNameSplit)-1]
            data.append([fileNameSplit[0],"." + fileExtension,"Generated",folderFilePath.replace(mainFolderToLogDir, ""),""])
            foundFiles += 1
    
    print("[kanban-automatic-logger] " + str(foundFiles) + " file(s) found.")
    trueFoundFiles += foundFiles

    if needToScanAgain == True:
        for folderPath in scanFolders:
            scanFolder(folderPath)

scanFolder(mainFolderToLogDir)

# This writes the new CSV file, it overwrites what's already there or creates a new one based on it's name.
splitDirectoryPath = mainFolderToLogDir.split("/")
outputName = splitDirectoryPath[len(splitDirectoryPath)-1]
with open("generated/"+outputName+".csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

print("[kanban-automatic-logger] Completed. " + str(folderCount) + " folder(s) with " + str(trueFoundFiles) + " files found.")