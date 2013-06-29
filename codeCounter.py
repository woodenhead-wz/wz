import os,sys

class codeCounter():
    def __init__(self):
        self.commentLine = 0
        self.codeLine = 0
        self.blankLine = 0
        self.sourceFileCount = 0
        self.allResult = []
        self.totalCommentLine = 0L
        self.totalCodeLine = 0L
        self.totalBlankLine = 0L
#         self.types = types
        
    def trim(self,docString):
        if not docString:
            return ''
        return docString.strip()
    
    #enter a filepath for calculate all file count
    #
    def calculateCodeCount(self,fileName):
#         print 'filename :',fileName
        if os.path.isdir(fileName):
            if not fileName.endswith('\\'):
                fileName += '\\'
            for file in os.listdir(fileName):
                if os.path.isdir(fileName+file):
                    self.calculateCodeCount(fileName + file)
                else:
                    self.countLine(fileName + file)
        else:
            self.countLine(fileName)
        
    def printFileCount(self):    
        print 'All file number is:',self.sourceFileCount
        print 'Blank line for all file is:',self.totalBlankLine
        print 'comment line for all file is:',self.totalCommentLine
        print 'code line for all file is:',self.totalCodeLine
        print '\n'
        file = open(r'counterResult.txt','w')
        for result in self.allResult:
            file.write(result)
        file.write('\n\n All file number is:'+str(self.sourceFileCount))
        file.write('\n Blank line for all file is:'+str(self.totalBlankLine))
        file.write('\n comment line for all file is:'+str(self.totalCommentLine))
        file.write('\n code line for all file is:'+str(self.totalCodeLine))
    
    #count file line:
    #code lile
    #comment line
    def countLine(self,fileName):
        
        dirName,tempFile = os.path.split(fileName)
        tempName,exten = os.path.splitext(tempFile)
#         print 'dirName: ', dirName,' filename:',fileName
#         print 'baseName:', tempName,' extension:',exten
        commentBegin = False
        if exten =='.cpp' or exten == '.h' or exten == '.java':
#             print 'open fle ',fileName
            file = open(fileName,'r')
            self.sourceFileCount += 1
            alllines = file.readlines()
#             print alllines
            for line in alllines:
                lineTrimed = line.strip()
                #blank line
                if (lineTrimed =='' or len(lineTrimed) == 1):
                    self.blankLine += 1
                #comment
                elif lineTrimed.startswith(r'//'):
                    self.commentLine += 1
                elif (lineTrimed.startswith(r'/*') and commentBegin == False):
                    self.commentLine += 1
                    commentBegin = True
                elif commentBegin == True:
                    self.commentLine += 1
                    if lineTrimed.endswith(r'*/'):
                        commentBegin = False
                #code line
                else:
                    self.codeLine += 1
        elif exten == '.py':
            file = open(fileName,'r')
            self.sourceFileCount += 1
            alllines = file.readlines()
#             print alllines
            for line in alllines:
                lineTrimed = line.strip()
                if (lineTrimed =='' or len(lineTrimed) == 1):
                    self.blankLine += 1
                elif lineTrimed.startswith(r'#'):
                    self.commentLine += 1
                else:
                    self.codeLine += 1
        else:
#             print 'file ',fileName,' type isn\'t support'
            return
        
       #calcualte lines for comment,line,blank
        print '\nin file ',fileName,' :'
        print 'comment lines = ', self.commentLine
        print 'blank   lines = ', self.blankLine
        print 'code    lines = ', self.codeLine
        self.allResult.append('\n\nin file '+fileName+' :')
        self.allResult.append('\ncomment lines = '+ str(self.commentLine))
        self.allResult.append('\nblank lines = '+ str(self.blankLine))
        self.allResult.append('\ncode lines = '+ str(self.codeLine))
        #counter the total line and set the file line to 0
        self.totalCommentLine += self.commentLine
        self.totalBlankLine += self.blankLine
        self.totalCodeLine += self.codeLine
        
        self.commentLine = 0
        self.blankLine = 0
        self.codeLine = 0
            
        
if __name__ == '__main__':
    fileName = raw_input("Please input file/dir to count:")
#     fileType = raw_input('Please input file type to to compile statistics(with space separate):')
#     types = fileType.split()
    counter = codeCounter()
    counter.calculateCodeCount(fileName)
    counter.printFileCount()
    needContinue = raw_input('Press any key to continue')
    