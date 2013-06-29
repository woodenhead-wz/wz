#coding=utf-8
from mimetypes import guess_type
from os import getcwd, makedirs, path, chdir
import glob
import os
import sys
import shutil
import stat
import traceback

Executables = []
Audios = []
Videos = []
Images = []
Docs = []
HTML = []
Compress = []
Text = []
PyScripts = []
Nokia = []
Torrent = []
ISO = []
Short = []
AdvanceAudio = []
Un = []
Disk = []
mainlist = [Executables,Audios,Videos,Images,Docs,HTML,Compress,Text,PyScripts,Nokia,Torrent,ISO,Short,Un]
mainlistn = ["Executables moved:\n","Audio files moved:\n","Videos moved:\n","Images moved:\n","Documents moved:\n","Webpages moved:\n","Compressed files moved:\n","Text files moved:\n","Python scripts moved:\n","Nokia files moved:\n","Torrent files moved:\n","ISO files moved:\n","Shortcuts moved:\n","Unknown files moved:\n"]
Errors = []
global dir

#==============================================================================================================
def fileInDir(fileName,dirName):
    for root,dirs,files in os.walk(dirName, topdown = False):
        for file in files:
            if fileName == file:
                return True
    return False 
#==============================================================================================================
def getDirSize(dirName):
    size = 0L
    for root,dirs,files in os.walk(dirName):
        size += sum([os.path.getsize(os.path.join(root,file)) for file in files])
    if size > 1024**2:
        print 'dir: ',dirName, ' size is ',size/1024/1024, 'MB'
    elif size > 1024:
        print 'dir: ',dirName, ' size is ',size/1024, 'KB' 
    else:
        print 'dir: ',dirName, ' size is ',size, "Bytes"
    return size
#==============================================================================================================
def changeFileMod(dirName):
    for root, dirs, files in os.walk(dirName):  
        for file in files:  
            if(not file[0] == "."):  
                fp=os.path.join(root, file)  
                print fp  
                os.chmod(fp, stat.S_IMODE(os.stat(fp)[stat.ST_MODE]) | stat.S_IRGRP | stat.S_IROTH )  
        for dir in dirs:  
            if(not dir[0] == "."):  
                dp = os.path.join(root, dir)  
                print dp  
                os.chmod(dp, stat.S_IMODE(os.stat(dp)[stat.ST_MODE])  | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)  
#==============================================================================================================
#move file to exact folder
def moveFile(fileName,dirName):
#     print 'in movefile, file = %s, dirname =%s'%(fileName,dirName)
    try:
        os.makedirs(str(dirName))
    except OSError:
#         print dirName, ' is already exist!'
        pass
    (x,y) = os.path.split(fileName)
#     print 'x,y:= ', x,y    
    fileAlreadyIndir = fileInDir(y,dirName)
    if fileAlreadyIndir == True and (not x == dirName):#if file already in dir, just remove the file in original folder
        try:
            os.remove(fileName)
            return
        except:
            pass
            return
#if file folder is as dir name,do nothing
    if x==dirName:
        return
    #else copy the file to exact dir
    try:
        shutil.move(str(fileName), str(dirName))
    except (shutil.Error, WindowsError):
#         traceback.print_exc()
        pass
    print 'move file : %20s to folder: %20s'%(fileName,dirName)
#==============================================================================================================       
def indentifyFileType(file,fileType):
    global dir
    type = str(fileType)
#     print 'in indentify',file,type
    (filepath,filename) = os.path.split(file)
#     print 'filepath = %s, filename= %s'%(filepath,filename)
#excutable
    if type in ["('application/octet-stream', None)","('application/x-sh', None)","('application/mac-binhex40', None)"] or filename.endswith('.msi'):
        moveFile(file,str(dir+'\Executable'))
        Executables.append(filename)
#Videos
    elif type in ["('video/x-msvideo', None)","('video/mp4', None)"] or filename.endswith('.webm') or filename.endswith('.flv'):
        moveFile(file,str(dir+r'\Videos'))
        Videos.append(filename)
#Images
    elif type in ["('image/x-png', None)","('image/pjpeg', None)","('image/gif', None)","('image/jpeg', None)"]:
        moveFile(file,str(dir+r'\Images'))
        Images.append(filename)
#Audio Basic        
    elif type in ["('audio/x-mpg', None)","('audio/x-wav', None)","('audio/x-ms-wma', None)","('midi/mid', None)"]: 
        moveFile(file,str(dir+r'\Audios'))
        Audios.append(filename)
#Documents
    elif type in ["('application/vnd.openxmlformats-officedocument.wordprocessingml.document', None)","('application/x-msexcel', None)",\
                "('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', None)",\
                "('application/x-mspowerpoint', None)","('application/x-mspowerpoint.12', None)",\
                "('application/msword', None)","('application/pdf', None)"] or filename.endswith('.pdf'):
        moveFile(file,str(dir+r'\Documents'))
        Docs.append(filename)
#Web Pages
    elif type in ["('text/html', None)"]:
        moveFile(file,str(dir+r'\Html'))
        HTML.append(filename)
#Compressed
    elif type in ["('application/x-tar', 'gzip')","('application/zip', None)",] or filename.endswith('.rar') or filename.endswith('.7z') or filename.endswith('.zip') or filename.endswith('.bz2') or filename.endswith('.tar'):
        moveFile(file,str(dir+r'\Compress'))
        Compress.append(filename)
#Text
    elif type in ["('text/plain', None)"]:
        if filename.endswith('.c') or filename.endswith('.h') or filename.endswith('.cpp'):
            moveFile(file,str(dir+r'\C_Cpp'))
        else:
            moveFile(file,str(dir+r'\Text'))
        Text.append(filename)
#Python Scripts :)
    elif type in ["('text/x-python', None)"]:
        moveFile(file,str(dir+r'\Python'))
        PyScripts.append(filename)
#Torrent files, you naughty dog :P
    elif type in ["('application/x-bittorrent', None)"]:
        moveFile(file,str(dir+r'\bitTorrent'))
        Torrent.append(filename)
#Shortcuts
    elif filename.endswith('.lnk'):
        moveFile(file,str(dir+r'\Shortcut'))
        Short.append(filename)
#Audio advanced
    elif filename.endswith('.flac') or filename.endswith('.FLAC'):
        moveFile(file,str(dir+r'\AdvancedAudio'))
        AdvanceAudio.append(filename)
#Disk Images
    elif filename.endswith('.ISO') or filename.endswith('.iso') or filename.endswith('.img') or filename.endswith('.IMG'):
        moveFile(file,str(dir+r'\Demo'))
        Disk.append(filename)
#Unknown
    else:
        if filename.endswith('.cpp'):
            moveFile(file,str(dir+r'\C_Cpp'))
        else:
            moveFile(file,str(dir+r'\Unknown'))
        Un.append(filename)
#==============================================================================================================        
#search *.txt/*.pdf like file and append to exact list variable
def identifyFileAndMove(dirName):
    global dir
    dir = dirName
    for dirPaths,dirNames,files in os.walk(dirName):
        print 'dirpath = %s'%dirPaths
        for file in files:
            fileType = guess_type(file)
            realfile = os.path.join(dirPaths,file)
#             print file,fileType
            indentifyFileType(realfile,fileType)
        
#==============================================================================================================    
def storeResult():
    pass       
#==============================================================================================================  
def removEmptyeDir(dir):
    for root, dirs, files in os.walk(str(dir), topdown=False):
#         print 'removed root is %s'%root
        if getDirSize(root) == 0:
            shutil.rmtree(root)
#==============================================================================================================  
if __name__ =='__main__':
    dirName = raw_input('please input folder to be clean:')
    identifyFileAndMove(str(dirName))

#remove empty folder
    removEmptyeDir(dirName)
#     if getDirSize(dirName) == 0:
#         os.rmdir(dirName)
    confirm = raw_input("Press any key to continue")
        