import csv
import os

# Directory to copy from.
mainFolderToLogDir = "" # Insert the file path of the folder you want to "copy"
outputDir = "generated"

# Base Data to hold every file as their name, stage will always be Generated, parent folder name, no note by default.
data = [["File Name", "File Type", "Stage", "Parent Folder", "Changes / Notes"]]

# Folders found to be scanned will be scanned here.
scanFolders = [mainFolderToLogDir]

# Scan the folder to import the data
def scanFolder(folderFilePath: str):
    print("[kanban-automatic-logger] Scanning " + folderFilePath)
    scanFolders.remove(folderFilePath)

    needToScanAgain = False
    for file in os.listdir(os.fsencode(folderFilePath)):
        filename = os.fsdecode(file)
        filePath = folderFilePath + "/" + filename
        realFile = os.fsencode(filePath)

        if os.path.isdir(realFile):
            # File is a folder/directory
            scanFolders.append(filePath)
            needToScanAgain = True
        else:
            print(filename)
            fileNameSplit = filename.split(".")
            data.append([fileNameSplit[0],"." + fileNameSplit[1],"Generated",folderFilePath.replace(mainFolderToLogDir, ""),""])
            # File is a file.
    
    if needToScanAgain == True:
        for folderPath in scanFolders:
            scanFolder(folderPath)

scanFolder(mainFolderToLogDir)

with open("generated/test1.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)