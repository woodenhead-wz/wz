#coding=utf-8
import os,sys,re
from PyQt4 import QtCore
from PyQt4.QtGui import *
from PyQt4.Qt import *
import urllib,urllib2
from bs4 import BeautifulSoup 

#the Tranaslate GUI
class googleTransWidget(QWidget):
    def __init__(self,parent = None):
        super(googleTransWidget,self).__init__(parent)
        self.setWindowTitle('Google Translator')
        self.resize(QSize(640,320))
        self.englishToChinese = True
        self.init()
        
    def init(self):
        self.vbox = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
         
        self.sourceLabel = QLabel('English')
        self.sourceLabel.setAlignment(Qt.AlignCenter) 
        self.destLabel = QLabel('Chinese')
        self.destLabel.setAlignment(Qt.AlignCenter) 
        self.changeDirButton = QPushButton('>>')
        self.hbox1.addWidget(self.sourceLabel,stretch =2)
        self.hbox1.addWidget(self.changeDirButton)
        self.hbox1.addWidget(self.destLabel,stretch =2)
        
        self.sourceText = QTextEdit()
        self.startButton = QPushButton('Translate')
        self.destText = QTextEdit()
        self.hbox2.addWidget(self.sourceText)
        self.hbox2.addWidget(self.startButton)
        self.hbox2.addWidget(self.destText)
         
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.setLayout(self.vbox)
        
        self.connect(self.changeDirButton, SIGNAL('clicked()'),self,SLOT('changeSourceDest()'))
        self.connect(self.startButton, SIGNAL('clicked()'),self,SLOT('startTranslate()'))
#         self.connect(self.sourceText, SIGNAL('returnPressed()'),self,SLOT('startTranslate()'))
        
    def setTranslator(self,translator):
        self.translator = translator
    
    @QtCore.pyqtSlot()
    def changeSourceDest(self):
        if self.sourceLabel.text() == 'English':
            self.sourceLabel.setText('Chinese')
            self.destLabel.setText('English')
            self.translator.setTransLang('zh-CN', 'en')
            self.englishToChinese = False
        else:
            self.sourceLabel.setText('English')
            self.destLabel.setText('Chinese')
            self.translator.setTransLang('en','zh-CN')
            self.englishToChinese = False
        
    @QtCore.pyqtSlot()
    def startTranslate(self):
        self.translator.translate(self.sourceText.toPlainText())

#=====================================================================================
#the translator
class googleTranslator():
    def __init__(self):
        self._url =  'http://translate.google.cn/translate_t' 
        self._s =None
        self._langFrom = 'en'
        self._langTo = 'zh-CN'
        self._strTranslated = None
        self. _strDic = None
    
    def setWidget(self,googleWidget):
        self.widget = googleWidget
        
    def translate(self,inputText):
        values = {self._langFrom:self._langTo, 'ie':'UTF-8', 'text':inputText, 'langpair':self._langFrom+'|'+self._langTo}
        data = urllib.urlencode(values)
        print data
        req = urllib2.Request(self._url,data)
        req.add_header('User-Agent', "Mozilla/4.0 (compatible; MSIE 6.0;Windows NT 5.1; SV1; .NET CLR 2.0.50727)")
        f = urllib2.urlopen(req)
        self._s = f.read()
#         print self._s
        f.close()
        html = BeautifulSoup(self._s) 
#         print html
        transDiv = html.find_all('div',dir="ltr")#,id='tts_button')
        self._transResult = self.findText(transDiv)
        self.widget.destText.setText(self._transResult)
        
    def findText(self, divs):
        for div in divs:
            foundDiv = div.find_all('div',id='tts_button')
            if not len(foundDiv) == 0:
                print div.get_text()
                return div.get_text()
        return None
    def setTransLang(self,transfrom,transto):
        self._langFrom = transfrom
        self._langTo = transto
        
    def getTranslatedText(self):
        return self._strTranslated
    
    def getDictText(self):
        return self._strDict
#=====================================================================================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    googleTranslateWidget = googleTransWidget()
    translator = googleTranslator()
    googleTranslateWidget.setTranslator(translator)
    translator.setWidget(googleTranslateWidget)
    googleTranslateWidget.show()
    app.exec_()
    