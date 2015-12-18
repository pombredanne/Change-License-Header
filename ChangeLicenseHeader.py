#!/usr/bin/env python
# -*- coding: utf-8 -*-
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
# 
# Copyright (c) 2015  Jeroen de Bruijn  <vidavidorra@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
#title           : ChangeLicenseHeader.py
#date created    : 2015/12/16
#python_version  : 3.5.1
#notes           :
__author__ = "Jeroen de Bruijn"
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Jeroen de Bruijn"
__email__ = "vidavidorra@gmail.com"

"""This program can change the license header inside files.
"""
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*

# Import the modules needed to run the script.
import sys, os, re
from argparse import ArgumentParser
from shutil import copyfile
import time

# Main definition - constants
licenseInfo="""ChangeLicenseHeader %s  Copyright (c) 2015  %s <%s>
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
""" %(__version__, __author__, __email__)
# for details type `show w'.
# type `show c' for details.
backupSuffix='.original'
processExtentions=('.c', '.h', '.cpp', '.hpp')
startLicenseHeader=" \*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*"
endLicenseHeader=' \*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*~\*\*/'
newLicense=''' *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
 * 
 * This file is part of LedCube.
 * 
 * Copyright (c) 2015  Jeroen de Bruijn  <vidavidorra@gmail.com>
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~**/'''

# =======================
#    FUNCTIONS
# =======================
def listFiles(walkDir, extentionList):
    print('Searching directories...')
    if not os.path.exists(walkDir):
        noticeError('Directory "%s" does not exist!' %os.path.abspath(walkDir))
        
    walkPath = os.path.abspath(walkDir)
    fileList = []
    
    for root, subdirs, files in os.walk(walkPath):
        print('Searching for files in directory %s' %os.path.abspath(root))
        
        for filename in files:
            if os.path.splitext(filename)[-1].lower() in extentionList:
                filePath = os.path.join(root, filename)
                fileList.append(filePath)
    
    return fileList

def processFiles(fileList, backupFlag):
    print('Processing files...')
    
    successFileList = []
    failedFileList = []
    
    for file in fileList:
        processResult = processFile(file, backupFlag)
        if processResult == 0:
            verifyResult = verifyChange(file)
            if verifyResult == 0:
                successFileList.append(os.path.abspath(file))
            else:
                failedFileList.append(os.path.abspath(file))
        else:
            failedFileList.append(os.path.abspath(file))
            
    return successFileList, failedFileList

def processFile(filename, backupFlag):
    print('Processing %s' %(os.path.abspath(filename)))
    result = verifyLicenseHeader(filename)
    if result == 1:
        return 1
    
    if backupFlag == True:
        # Backup files
        filePath, ext = os.path.splitext(filename)
        newFile = os.path.join(filename, filePath + ext + backupSuffix)
        copyfile(filename, newFile)
        
    with open(filename, 'r+') as file:
        fileContent = re.sub(startLicenseHeader + '.*?' + endLicenseHeader, newLicense, file.read(), flags=re.DOTALL)
        file.seek(0)
        file.write(fileContent)
        # Delete the rest of the file's content.
        file.truncate()
    
    return 0

def verifyLicenseHeader(filename):
    with open(filename, 'r') as file:
        match = re.search(startLicenseHeader + '.*?' + endLicenseHeader, file.read(), flags=re.DOTALL)
        
    if match is not None:
        return 0
    else:
        return 1

def verifyChange(filename):
    with open(filename, 'r') as file:
        match = re.search(startLicenseHeader + '.*?' + endLicenseHeader, file.read(), flags=re.DOTALL)
    
    if match.group(0) != newLicense:
        return 1
    else:
        return 0

def removeBackups(fileList):
    print('Deleting files...')
    deletedList = []
    
    for file in fileList:
        try:
            print('Deleting %s' %(os.path.abspath(file)))
            os.remove(file)
            deletedList.append(file)
        except OSError as e:
            if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
                raise # re-raise exception if a different error occured
    
    return deletedList

def printResults(fileList, successFileList, failedFileList, deletedFileList):
    print('\nSuccessfully changed license for file(s)')
    if successFileList == []:
        print('  None')
    else:
        for successFile in successFileList:
            print('  %s' %os.path.abspath(successFile))
    
    print('Could not change license for file(s)')
    if failedFileList == []:
        print('  None')
    else:
        for failedFile in failedFileList:
            print('  %s' %os.path.abspath(failedFile))
    
    print('Deleted file(s)')
    if deletedFileList == []:
        print('  None')
    else:
        for deletedFile in deletedFileList:
            print('  %s' %os.path.abspath(deletedFile))
        
    print('\nTotal processed %d file(s)' %len(fileList))
    print('Changed license in %d file(s)' %len(successFileList))
    print('Could not change license in %d file(s)' %len(failedFileList))
    print('Deleted %d file(s)' %len(deletedFileList))
    print('See log above for more information')


# =======================
#    HELPER FUNCTIONS
# =======================
def exit():
    print('*** ChangeLicenseHeader has finished')
    sys.exit()

def clearScreen():
    if os.name != "posix":
        os.system('cls')
    else:
        os.system('clear')

def noticeError(err):
    print('Error %s' %err)
    exit()

class Logger(object):
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w")
        self.log.write('Log file for ChangeLicense.py\n')
        self.log.write(time.strftime('%A, %B %d, %Y  %H:%M:%S UTC%z\n\n'))

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass
        
    def __del__(self):
        self.log.close()


# =======================
#    ARGUMENT PARSER
# =======================
def initializeParser():
    parser = ArgumentParser(description='Change the license header in files.')
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('folder',
        help='The folder to process recursively.')
    group.add_argument('--backup', action='store_true',
        help='Create backups of the input files before alternating them.')
    group.add_argument('--removeBackups', action='store_true',
        help='Remove previously created backups.')
    parser.add_argument('--logFile',
        help='Enable logging in a logfile. Note that this file will be emptied if it already exists.')
    
    return parser

# =======================
#    MAIN PROGRAM
# =======================
if __name__ == "__main__":
    parser = initializeParser()
    args = parser.parse_args()
    
    print(licenseInfo)

    
    if args.logFile != None:
        sys.stdout = Logger(args.logFile)
     
    if args.removeBackups == True:
        fileList = listFiles(args.folder, backupSuffix)
        deletedFileList = removeBackups(fileList)
        printResults(fileList, [], [], deletedFileList)
        exit()
    
    fileList = listFiles(args.folder, processExtentions)
    successFileList, failedFileList = processFiles(fileList, args.backup)
    printResults(fileList, successFileList, failedFileList, [])
        
    exit()
