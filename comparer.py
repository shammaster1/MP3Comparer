from tinytag import TinyTag
import itertools
from collections import Counter
import os
import shutil

#get all songs and meta data from folder 1
def first_folder(path1):
    songs1 = []
    songs1.append(path1)
    os.chdir(path1)
    for x in os.listdir(path1): # for files in directory
        if x.endswith(".mp3"):
            # append only mp3s to list
            songs1.append(x + ", " + str(TinyTag.get(x)))
    return songs1

#get all songs and meta data from folder 2
def second_folder(path2):
    songs2 = []
    songs2.append(path2)
    os.chdir(path2)
    for x in os.listdir(path2): # for files in directory
        if x.endswith(".mp3"):
            # append only mp3s to list
            songs2.append(x + ", " + str(TinyTag.get(x)))
    return songs2

#compare the folders to see which files are missing from which
#USES ALL ID3 DATA
def fullCompare(folder1, folder2):
    choice = input("\nWould you like to find what is missing from: \n1. " + folder1[0] + " compared to " + folder2[0] + 
                   "\n===OR===\n2. " + folder2[0] + " compared to " + folder1[0] + "\nEnter the number of your choice: >")
    count = 0
    missingTitle = []
    if choice == "1":
        missing = Counter(itertools.chain(folder2)) - Counter(itertools.chain(folder1))
        missing = list(missing.elements())
        # printing result
        print ("\nThe songs missing from " + folder1[0] + " are:\n")
        if len(missing) == 0:
            print("None! All MP3s Match")
        else:
            for x in missing[1:]:
                count += 1
                print(str(count) + ". " + x)
                print("\n")
                missingTitle.append(x.split(".mp3")[0])
        missingTitle.append("1")
    elif choice == "2":
        missing = Counter(itertools.chain(folder1)) - Counter(itertools.chain(folder2))
        missing = list(missing.elements())
        # printing result
        print ("\nThe song(s) missing from " + folder2[0] + " are:\n")
        if len(missing) == 0:
            print("None! All MP3s Match")
        else:
            for x in missing[1:]:
                count += 1
                print(str(count) + ". " + x)
                print("\n")
                missingTitle.append(x.split(".mp3")[0])
        missingTitle.append("2")
    print("Total: " + str(count) + "\n")
    return missingTitle

def copyFiles(filenames, origin, destination):
    filenames.pop(-1)
    for x in filenames:
        file_to_copy = str(origin) + "/" + x + ".mp3"
        # Specify the path of the destination directory you want to copy to
        destination_directory = str(destination)
        # Use the shutil.copy() method to copy the file to the destination directory
        shutil.copy(file_to_copy, destination_directory)
    print("\nThe following files have been successfully copied over: ")
    count = 0
    for x in filenames:
        count += 1
        print(str(count) + ". " + x)
    return

#FIX, add option to do vice versa or neither
def inputCopyFiles(origin, destination):
    choice = input("\nCONFIRM: Copy all listed files from '" + origin + "' to the path '" + destination + "'? (y/n):\n>")
    valid = False
    while valid == False:
        if choice in ['y', 'Y', 'n', 'N']:
            valid = True
        else:
            choice = input("Please enter a valid character: (y/n)>")
    if choice == 'y' or 'Y':
        return 1
    else:
        return 0

def filesWithNulls(fileData, path):
    os.chdir(path)
    fileData.pop(0)
    count = 0
    fileDataList = []
    print("\nFiles with empty metadata:\n")
    for x in fileData:
        tag = TinyTag.get(str(x.split(".mp3")[0] + ".mp3"))
        if tag.album == None or tag.albumartist == None or tag.artist == None or tag.genre == None or tag.title == None or tag.track == None or tag.year == None:
            fileDataList.append(str(count+1) + ". " + x.split(".mp3")[0] + ".mp3")
            count +=1
            print(str(count) + ". " + x.split(".mp3")[0] + ".mp3")
    if count == 0:
        print("None! All MP3s have an album, album artist, artist, genre, title, track, and year.")
    print("\n")
    return fileDataList

def main():
    # menu functionality implemented here
    cwd = os.getcwd()
    end = False # exits menu if true
    valid = False # checks if menu option chosen is valid, if not, reprompt
    while end == False:
        # menu start
        choice = input("\nWhat would you like to do (enter # option)?\n1. Compare Folders\n2. Find MP3s with missing data\n3. Exit\n>")
        # menu option prompt
        while valid == False:
            if choice not in ["1", "2", "3", "4"]:
                choice = input("Please enter a valid choice:\n>")
            else:
                valid = True
        # folder comparison option (1)
        if choice == "1":
            # obtain path for folder 1
            path1 = input("Please enter the path of folder 1: \n>")
            folder1_data = first_folder(path1)
            # obtain path for folder 2
            path2 = input("Please enter the path of folder 2: \n>")
            folder2_data = second_folder(path2)
            # compare folders
            completeList = fullCompare(folder1_data, folder2_data)
            choice1 = input("\nWould you like to copy over these missing files? (y/n)\n>")
            valid1 = False
            # ensure input is valid
            while valid1 == False:
                if choice1 not in ['y', 'Y', 'n', 'N']:
                    choice1 = input("Please enter a valid choice:\n>")
                else:
                    valid1 = True
            if choice1 in ['y', 'Y']:
                # missing files will be copied to folder 1
                if completeList[-1] == "1":
                    if inputCopyFiles(path2, path1) == 1:
                        copyFiles(completeList, path2, path1)
                    else:
                        print("Copying Canceled")
                # missing files will be copied to folder 2
                elif completeList[-1] == "2":
                    if inputCopyFiles(path1, path2) == 1:
                        copyFiles(completeList, path1, path2)
                    else:
                        print("Copying Canceled")
                # failsafe
                else:
                    raise Exception("Error: Path could not be found")
        # missing metadata option (2)
        elif choice == "2":
            pathChoice2 = input("\nEnter the directory you would like to check:\n>")
            # read folder data
            folder1_data = first_folder(pathChoice2)
            # see function for specifications
            songList = filesWithNulls(folder1_data, pathChoice2)
            printChoice2 = input("\n Would you like to create a .txt file to list all results? (y/n)\n>")
            valid2 = False
            while valid2 == False:
                if printChoice2 not in ['y', 'Y', 'n', 'N']:
                    printChoice2 = input("Please enter a valid choice:\n>")
                else:
                    valid2 = True
            if printChoice2 in ['y', 'Y']:
                file_name = "songList.txt"
                validDestination = False
                listDestination = input("Enter the destination .txt file:\n")
                while validDestination == False:
                    try:
                        os.chdir(listDestination)
                        validDestination = True
                    except:
                        listDestination = input("Please enter a valid path for the destination:\n")
                # Open the file in write mode
                with open(file_name, 'w', encoding="utf-8") as file:
                    file.write("===== Songs Missing Meta Data =====\n")
                    for x in songList:
                        file.write(x + "\n")
                    file.close()
                print(file_name + " created successfully at " + str(listDestination) + ".")
        # exits program
        elif choice == "3":
            end = True
            print("Thank you for using this program!")
main()