#coding=utf-8
from bs4 import BeautifulSoup  
import re,base64, json
import urllib2
import ConfigParser

PAGE_PREFIX = 'http://www.weather.com.cn/weather/'
PAGE_POSTFIX = '.shtml'
pageId = 0
cityDict ={}
#==============================================================================================
def parseSettingFile(fileName):
    cf = ConfigParser.ConfigParser()
    cf.read(fileName)
    s = cf.sections()
    citys = cf.options('city')
    for city in citys:
        citycode = cf.get('city',city)
        cityDict[city] = citycode
#==============================================================================================
def findCityCode(cityName):
    citycode = cityDict[cityName]
    return citycode
#==============================================================================================
def getCityWeather(cityId):
#     print 'page url: ',PAGE_PREFIX + cityId + PAGE_POSTFIX
    page = urllib2.urlopen(PAGE_PREFIX + cityId + PAGE_POSTFIX)
    pageHtml = page.read().decode('utf-8')
    print pageHtml
    soup = BeautifulSoup(pageHtml)
    title = soup.html.head.title
    print title.get_text()
    futureWeather = soup.find('div',class_="weatherYubaoBox")
    dayWeathers = futureWeather.find_all('table',class_='yuBaoTable')
    for eachWeather in dayWeathers:
        getEachdayWeather(eachWeather)
#==============================================================================================        
def getEachdayWeather(eachDayWeather):
    dayContent = ''
    date = eachDayWeather.find('td', class_='t0')
#     print date.get_text()
    dayAndNight = date.parent.parent
    tr_s = dayAndNight.find_all('tr')
    for tr in tr_s:
        td_s = tr.find_all('td')
        for td in td_s:
            td_content = td.get_text().strip().lstrip() 
            dayContent += td_content
            dayContent += '  '
    print unicode(dayContent)
#==============================================================================================  
if __name__ == '__main__':
    parseSettingFile('city.ini')
    cityname =raw_input('please input city name:')
    try:
        citycode = cityDict[cityname]
    except:
        print 'can\'t find city name in config file' 
    else:
        getCityWeather(citycode)
    input = raw_input('enter to continue:')
