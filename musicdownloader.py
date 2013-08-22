#coding=utf8
from bs4 import BeautifulSoup
import Queue
import getopt
import os
import re
import socket
import sys
import threading
import urllib
import urllib2

queue = Queue.Queue(0)#to store song list
DOWNLOAD_THREAD_NUMBER = 5#5 thread to download mp3
DIR_PREFIX = u'e:\\mp3\\'
baiduMusicUrl = 'http://music.baidu.com'
artistUrl = 'http://music.baidu.com/artist'

#############################################################################
#
# song class for store music information, name/author/length/artistUrl
#
#############################################################################
class Song():
    def __init__(self,name,author,length,songurl,downloadUrl,lrcurl):
        self.name = name
        self.author = author
        self.length = length
        self.url = songurl
        self.downloadUrl = downloadUrl
        self.lrcurl = lrcurl
    def setName(self,name):
        self.name = name
    def setAuthor(self,author):
        self.author = author
    def setLength(self,length):
        self.length = length
    def setSongUrl(self,songUrl):
        self.url = songUrl
    def setDownloadUrl(self,downloadUrl):
        self.downloadUrl = downloadUrl
    def setlrcUrl(self,lrcUrl):
        self.lrcurl = lrcUrl
#############################################################################
#
# download thread
#
#############################################################################  
class HttpDownloadThread(threading.Thread):
    def __init__(self,queue,dir):
        self.jobq = queue
        self.dirName = dir
        threading.Thread.__init__(self)
    def run(self):
        while True:
            if self.jobq.qsize() > 0:
                print 'jobq size = ',self.jobq.qsize()
                job = self.jobq.get()
                self.processJob(job)
            else:
                break
    def processJob(self,job):
        download(self.dirName,job)

#############################################################################
#
# util function,for download mp3
#
############################################################################# 
def cbk(a, b, c):
    '''回调函数
    @a: 已经下载的数据块
    @b: 数据块的大小
    @c: 远程文件的大小
    '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print '%s downloading %.2f%%' %(threading.currentThread().name, per)
        
def download(dirName,job):
#     print 'dir=%s, job=%s'%(dirName,job.name)
    songName = job.name
    songNameList = job.name.split('/')
    if len(songNameList) > 1:
        songName = songNameList[-1]
    try:
        urllib.urlretrieve(job.downloadUrl,dirName+'/'+songName+'.mp3',cbk)
    except Exception,e:
        print 'cant retrieve %s'%songName
#############################################################################
#
# util function,for split array
#
############################################################################# 
def splitArray(string,separator):
    return string.split(separator)
#############################################################################
#
# page parser class, use beautifulsoup parse content
#
#############################################################################      
class SongParser():
    def __init__(self,artistUrl,artistName):
        self.url = artistUrl
        self.artistName = artistName
        self.songUrlList=[]
        self.songList = []
        
    #get main page of artist
    def getPage(self):
        try:
            result = urllib2.urlopen(self.url)
            self.pageContent = result.read()
        except Exception,e:
            print 'Can\'t open url:',self.url
    #get artist song list, now 20 songs
    def getSongURLList(self):
        soup = BeautifulSoup(self.pageContent)
        songUrlHrefList = soup.findAll('a',href=re.compile(u'/song//*'))
        print songUrlHrefList
        for songHrefUrl in songUrlHrefList:
            songid = songHrefUrl['href']
            songName = songHrefUrl['title']
            songUrl = baiduMusicUrl + songid
            asong = Song(name=songName,author=self.artistName,length=None,songurl=songUrl,downloadUrl=None,lrcurl=None)
#             self.songUrlList.append(songUrl)
            self.songList.append(asong)
        for a in self.songList:
            print a.name,a.author,a.url
         
    #save the download url to queue   
    def saveSongs(self):
        for song in self.songList:
#         for songUrl in self.songUrlList:
            result = urllib2.urlopen(song.url)
            page = result.read()
            soup = BeautifulSoup(page)
            downloadUrlElement = soup.findAll('a',attrs={'download_url' : re.compile('http://*')})
            if len(downloadUrlElement):
                downloadUrl = downloadUrlElement[0]['download_url']
                global queue
                song.setDownloadUrl(downloadUrl)
                queue.put(song)
        
#############################################################################
#
# get artist id according artist name
#
############################################################################# 
def getArtistIdByName(name):
    global artistUrl
    result = urllib2.urlopen(artistUrl, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT)
    pageContent = result.read()
    print 'in getArtistIdByName, name:',name
    soup = BeautifulSoup(pageContent)
    artist = soup.findAll('a',text=name)
    print 'artist url:',artist
    if len(artist) > 0:
        artistHref = artist[0]['href']
        stringlist = artistHref.split('/')
        if len(stringlist) == 3:
            return stringlist[2]
    return None
#############################################################################
#
# main function
#
############################################################################# 
def main():
    #first we parse artist name 
#     try:
#         options,args = getopt.getopt(sys.argv[1:],'hp:a:',['help','artist='])
#     except getopt.GetoptError:
#         print 'get option error, exit program'
#         sys.exit(1)
#     for name,value in options:
#         print 'name=%s,value=%s'%(name,value)
#         if name in ('-h','--help'):
#             print 'Help'
#         if name in ('-a','--artist'):
#             print 'artist is ',value
#             artistName = value
    artistName = unicode(raw_input("Please input artist name:").encode(sys.stdin.encoding))
    if artistName is None or len(artistName)==0:
        print 'artist name can\'t be null'
    if not os.path.exists(DIR_PREFIX+artistName):
        os.makedirs(DIR_PREFIX+artistName)
        
    #get artist URL accroding name
    id = getArtistIdByName(unicode(artistName))
    print 'artist id in baidu music is ',id
    if(id is None):
        print 'cant get artist id, exit!'
        exit(1)
    global artistUrl
    artistUrl = artistUrl + '/' + id
    print 'artist url in baidu music: ',artistUrl
    
    #get song download url and store in queue
    parser = SongParser(artistUrl,artistName)
    parser.getPage()
    parser.getSongURLList()
    parser.saveSongs()
    
    global queue
    print 'queue size = ',queue.qsize()
    
    #download mp3 in multithread
    for x in range(DOWNLOAD_THREAD_NUMBER):
        HttpDownloadThread(queue,DIR_PREFIX+artistName).start()
#############################################################################
#
# run 
#
############################################################################# 
if __name__ =='__main__':
    main()
