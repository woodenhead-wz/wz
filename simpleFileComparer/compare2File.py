# -*- coding: utf-8 -*-
import os;
import shutil

folderA = raw_input('Please input before modified folder:').lower()
folderB = raw_input('Please input after modified folder:').lower()

filePathsA = []
filePathsB = [] 

appendedFiles = []
modifiedFiles = []

for dirpath,dirnames,filenames in os.walk(folderA):
    for filename in filenames:
        filePathA = dirpath+'\\'+filename
        filePathsA.append(filePathA)
        
for dirpath,dirnames,filenames in os.walk(folderB):
    for filename in filenames:
        filePathB = dirpath + '\\' + filename
        filePathsB.append(filePathB)
        
for filepath in filePathsB:
    print filepath
    fileBLen = len(folderB)
    fileNameB = filepath[fileBLen:] #get file path in B folder
    filePathToA = folderA + fileNameB #get mapping file in A
    print 'file path to A is: ',filePathToA
    
    if filePathToA not in filePathsA:
        appendedFiles.append(filepath)
        continue
    
    fileA = open(filePathToA,'rb')
    textA = fileA.read()
    fileA.close()
    
    fileB = open(filepath,'rb')
    textB = fileB.read()
    fileB.close()
    
    if textA != textB:
        modifiedFiles.append(filepath)

output = open('result.txt','wb')
output.write('added files :\n')
for appendfile in appendedFiles:
    output.write(appendfile + '\n')
    
output.write('modified files: \n')
for modifiedfile in modifiedFiles:
    output.write(modifiedfile + '\n')
    
if len(appendedFiles)>0 or len(modifiedFiles)>0:
    choise = raw_input('Do you want to overwrite original Files: Y/N')
    if choise == 'Y':
        for appendfile in appendedFiles:
            shutil.copy2(appendfile, folderA)
            print 'copy %s to %s successful!'%(appendfile,folderA)
        for modifiedfile in modifiedFiles:
            shutil.copy2(modifiedfile, folderA)

    
     
