# Change License Header
[![License GPLv3][badge-license]][license]

Script to change the license header in files. This could be usefull if you want to change the license for your project and need to change the licence header in all your `.c` and `.h` files for example. It changed the license in a file and then checks the change by opening the file (again) and verifying that the licence header is actually changed.

# Usage
```
usage: ChangeLicenseHeader.py [-h] [--backup | --removeBackups]
                              [--logFile LOGFILE]
                              folder

Change the license header in files.

positional arguments:
  folder             The folder to process recursively.

optional arguments:
  -h, --help         show this help message and exit
  --backup           Create backups of the input files before alternating
                     them.
  --removeBackups    Remove previously created backups.
  --logFile LOGFILE  Enable logging in a logfile. Note that this file will be
                     emptied if it already exists.
```

# Example
```
C:\Users\jdebruijn\Drive\Programming\Python\ChangeLicenseHeader>ChangeLicenseHeader.py --backup --logFile myLog.log source
ChangeLicenseHeader 1.0.0  Copyright (c) 2015  Jeroen de Bruijn <vidavidorra@gmail.com>
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.

Searching directories...
Searching for files in directory C:\Users\jdebruijn\Drive\Programming\Python\ChangeLicenseHeader\source
Searching for files in directory C:\Users\jdebruijn\Drive\Programming\Python\ChangeLicenseHeader\source\src
Processing files...
Processing C:\Users\jdebruijn\Drive\Programming\Python\ChangeLicenseHeader\source\header1.h
Processing C:\Users\jdebruijn\Drive\Programming\Python\ChangeLicenseHeader\source\src\main.c

Successfully changed license for file(s)
  C:\Users\jdebruijn\Drive\Programming\Python\ChangeLicenseHeader\source\header1.h
  C:\Users\jdebruijn\Drive\Programming\Python\ChangeLicenseHeader\source\src\main.c
Could not change license for file(s)
  None
Deleted file(s)
  None

Total processed 2 file(s)
Changed license in 2 file(s)
Could not change license in 0 file(s)
Deleted 0 file(s)
See log above for more information
*** ChangeLicenseHeader has finished
```


# Licensing
GNU General Public License version 3 or later, as published by the Free Software Foundation.
Modification and redistribution are permitted according to the terms of the GPL.
The license can be found in the `LICENSE` file.


[badge-license]:                        https://img.shields.io/badge/license-GPLv3-blue.svg
[license]:                              https://github.com/vidavidorra/Change-License-Header/blob/master/LICENSE
