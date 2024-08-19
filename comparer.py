from tinytag import TinyTag
import itertools
from collections import Counter
import os
import shutil

#get all mp3s and meta data from folder 1
def folderData(path1):
    mp3s = []
    mp3s.append(path1)
    os.chdir(path1)
    for x in os.listdir(path1): # for mp3s in directory
        if x.endswith(".mp3"):
            # append only mp3s to list
            mp3s.append(x + ", " + str(TinyTag.get(x)))
    return mp3s

#compare the folders to see which mp3s are missing from which
#USES ALL ID3 DATA
def fullCompare(folder1, folder2):
    choice = input("\nWould you like to find what is missing from: \n1. " + folder1[0] + "\n===OR===\n2. " + folder2[0] + "\nEnter the number of your choice:\n>")
    count = 0
    missingTitle = []
    if choice == "1":
        missing = Counter(itertools.chain(folder2)) - Counter(itertools.chain(folder1))
        missing = list(missing.elements())
        # printing result
        print ("\nThe MP3(s) missing from " + folder1[0] + " are:\n")
        if len(missing) == 0:
            print("None! All MP3(s) Match")
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
        print ("\nThe MP3(s) missing from " + folder2[0] + " are:\n")
        if len(missing) == 0:
            print("None! All MP3(s) Match")
        else:
            for x in missing[1:]:
                count += 1
                print(str(count) + ". " + x)
                print("\n")
                missingTitle.append(x.split(".mp3")[0])
        missingTitle.append("2")
    print("Total: " + str(count) + "\n")
    return missingTitle

# copy all differing mp3s to a specified folder destination
def copyMP3s(mp3Names, origin, destination):
    mp3Names.pop(-1)
    count = 0
    print("\nThe following MP3(s) have been successfully copied over: ")
    for x in mp3Names:
        count += 1
        mp3ToCopy = str(origin) + "/" + x + ".mp3"
        # Specify the path of the destination directory you want to copy to
        destinationDirectory = str(destination)
        # Use the shutil.copy() method to copy the mp3 to the destination directory
        shutil.copy(mp3ToCopy, destinationDirectory)
        print(str(count) + ". " + x)
    return

# prompt for confirming copy process
def inputCopyMP3s(origin, destination):
    choice = input("\nCONFIRM: Copy all listed MP3(s) from '" + origin + "' to the destination '" + destination + "'? (y/n):\n>")
    valid = False
    while valid == False:
        if choice in ['y', 'Y', 'n', 'N']:
            valid = True
        else:
            choice = input("Please enter a valid character: (y/n)\n>")
    if choice in ['y', 'Y']:
        return 1
    elif choice == ['n', 'N']:
        return 0

# list all mp3s with missing metadata
def mp3sWithNulls(mp3Data, path):
    os.chdir(path)
    mp3Data.pop(0)
    count = 0
    mp3DataList = []
    print("\n\nMP3(s) with empty metadata:\n")
    for x in mp3Data:
        tag = TinyTag.get(str(x.split(".mp3")[0] + ".mp3"))
        # fields of missing metadata to include
        if tag.album == None or tag.albumartist == None or tag.artist == None or tag.genre == None or tag.title == None or tag.track == None or tag.year == None:
            mp3DataList.append(str(count+1) + ". " + x.split(".mp3")[0] + ".mp3")
            count +=1
            print(str(count) + ". " + x.split(".mp3")[0] + ".mp3")
    if count == 0:
        print("None! All MP3(s) have an album, album artist, artist, genre, title, track, and year.\n")
    return mp3DataList

# menu option 1: obtain two paths, compare the folders, list differences, and optionally, copy over all missing mp3s
def menuChoice1():
    # obtain path for folder 1
    path1 = input("Please enter the path of folder 1: \n>")
    folder1Data = folderData(path1)
    # obtain path for folder 2
    path2 = input("Please enter the path of folder 2: \n>")
    folder2Data = folderData(path2)
    # compare folders
    completeList = fullCompare(folder1Data, folder2Data)
    choice1 = input("\nWould you like to copy over these missing MP3(s)? (y/n)\n>")
    valid1 = False
    # ensure input is valid
    while valid1 == False:
        if choice1 not in ['y', 'Y', 'n', 'N']:
            choice1 = input("Please enter a valid choice:\n>")
        else:
            valid1 = True
    if choice1 in ['y', 'Y']:
        # missing mp3s will be copied to folder 1
        if completeList[-1] == "1":
            copyToPath1 = inputCopyMP3s(path2, path1)
            if copyToPath1 == 1:
                copyMP3s(completeList, path2, path1)
            else:
                print("Copying Canceled")
        # missing mp3s will be copied to folder 2
        elif completeList[-1] == "2":
            copyToPath2 = inputCopyMP3s(path1, path2)
            if copyToPath2 == 1:
                copyMP3s(completeList, path1, path2)
            else:
                print("Copying Canceled")
        # failsafe
        else:
            raise Exception("Error: Path could not be found")
    return

# list all mp3s in a folder that are missing metadata, and optionally, create a .txt file where specified
def menuChoice2():
    pathChoice2 = input("\nEnter the directory you would like to check:\n>")
    # read folder data
    folder1Data = folderData(pathChoice2)
    # see function for specifications
    mp3List = mp3sWithNulls(folder1Data, pathChoice2)
    printChoice2 = input("\n Would you like to create a .txt file to list all results? (y/n)\n>")
    valid2 = False
    while valid2 == False:
        if printChoice2 not in ['y', 'Y', 'n', 'N']:
            printChoice2 = input("Please enter a valid choice:\n>")
        else:
            valid2 = True
    # create .txt file
    if printChoice2 in ['y', 'Y']:
        fileName = input("Enter the desired name of the .txt file: (enter nothing for default name 'mp3List.txt'):\n>")
        if fileName == "":
            fileName = "mp3List.txt"
        else:
            fileName = fileName + ".txt"
        validDestination = False
        listDestination = input("Enter the destination .txt file:\n>")
        while validDestination == False:
            try:
                os.chdir(listDestination)
                validDestination = True
            except:
                listDestination = input("Please enter a valid path for the destination:\n>")
        # Open the file in write mode
        with open(fileName, 'w', encoding="utf-8") as file:
            file.write("Searched folder: "+ pathChoice2)
            file.write("\n===== MP3(s) Missing Meta Data =====\n")
            for x in mp3List:
                file.write(x + "\n")
            file.close()
        print(fileName + " created successfully at " + str(listDestination) + ".")
    return

# exits the menu
def menuChoice3():
    end = True
    print("Thank you for using this program!")
    return

def main():
    # menu functionality implemented here
    cwd = os.getcwd()
    end = False # exits menu if true
    while end == False:
        # menu start
        choice = input("\nWhat would you like to do? (enter # option)\n1. Compare Folders\n2. Find MP3(s) with missing data\n3. Exit\n>")
        # menu option prompt
        valid = False # checks if menu option chosen is valid, if not, reprompt
        while valid == False:
            if choice not in ["1", "2", "3", "4"]:
                choice = input("Please enter a valid choice:\n>")
            else:
                valid = True
        # folder comparison option (1)
        if choice == "1":
            menuChoice1()
        # missing metadata option (2)
        elif choice == "2":
            menuChoice2()
        # exits program
        elif choice == "3":
            end = menuChoice3()
    return

main()