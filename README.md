# MP3Comparer

## Description

Finds MP3s missing when comparing two folders and copies over missing files if prompted. Also finds MP3s that are missing tag data (view "Details" below for what "missing tag data" is defined as) and gives the option to create a .txt of the list.

Example of folder comparison:

- folder 1:\
  ![alt text](image_examples/ex1.jpg "Folder 1")
- folder 2:\
  ![alt text](image_examples/ex2.jpg "Folder 2")
- result of comparing folder 2 to 1:\
  ![alt text](image_examples/ex3.jpg "Result")

Example of missing meta data finder:

- folder:\
  ![alt text](image_examples/ex4.jpg "Folder")
- result of missing meta data finder:\
  ![alt text](image_examples/ex5.jpg "Result")

## Details

Missing tag data is defined as songs missing one of the following: album, album artist, artist, genre, title, track, or year.

## Requirements

Python 3.6 or greater\
[tinytag](https://pypi.org/project/tinytag/)
