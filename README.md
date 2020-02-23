# photo-sorter-namer
get all the files of specific types from a directory and its sub directories, and rename them all to have the same format.
Customizable date formatting, add name based on range of dates


## Helpme what does this do ↓

Source path: root folder, all files in subfolder are checked

File types: file types that are effected by sorter

Check: shows how many files have been found

Destination path:  folder where all the files will be copied to


### Name format:

format that the files will be named in,
uses strftime formats ( https://strftime.org/ )
as well as 2 custom formats:


**%o** : original file name

**%r** : range name


### Ranges:

Add a word to file names based on when they were created
allows for files made within certain time ranges to be named differently
(e.g: 01-01-2013 to 31-12-2018 = "Highschool")


name: word that will be added to file name

Start date, end date: range of dates that the word will be applied to
