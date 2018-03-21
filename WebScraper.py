################################################################################################
# Title:         Webscarper
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   accesses the internet for webpages and performs intermediary parsing
# Arguments:     testID, database connection, webpage URL
# Sub-processes: timer
################################################################################################
#! urs/bin/python3

import GeneralProcesses, tests, urllib, re, urllib.request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup



################################################################################
# Title:         fileRequest
# Author:        Michael Grant
# Date:          Sept 2017
# Description



################################################################################
# Title:         fileRequest
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   checks URL for validity makes a HTTP GET request for the resource.  
# Arguments:     URL
# Sub-processes: none
################################################################################


def fileRequest(URL):
 #  print("This is the fileRequest process")
   # check to determine if URL is valid

   html = []
   if re.match(r'[hH][tT][tT][pP][sS]?://[a-z.+-/?]',URL):
      searchURL = URL
#      print(searchURL)
   elif (re.match(r'[a-z.+-/_?]+',URL)):
      searchURL = 'http://' + URL
#      print(searchURL)
   else:
      searchURL = None
   if searchURL:
      try:
         with urllib.request.urlopen(searchURL) as responce:
            html =responce.read()
      except HTTPError :
         html = None
      except URLError:
         html = None
   return html


def buildLink(link,URL):
   sLink =str(link)
   if re.match(r'[hH][tT][tT][pP][sS]?://[a-zA-Z0-9.+-/?\[\]%+-_]+',sLink):
      return sLink
   if re.match(r'//[a-zA-Z0-9/?\[\]()%!+-_]+',sLink):
      return sLink[2:len(sLink)+1]
   if re.match(r'/[a-zA-Z0-9]+[a-zA-Z0-9/?\[\]%+-_]+',sLink):
      return URL+sLink

   return None


################################################################################
# Title:         intermediateParser
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   Parses retrieved file into needed meta-data files
# Arguments:     testID, raw html file
# Sub-processes: None
################################################################################

def intermediateParser(connection,testID,pageID,html,URL):
   print("This is the intermediateParser")
   
   soupHTML = BeautifulSoup(html,'html.parser')
   potentialLinks = []
   linksegment=' '
   tagList = []
   contentList =[]
   imgLinks = []
   tags = ''

   # get all internal links
   count =0
   RE = r'[a-zA-Z0-9/?\[\]()%!+-_]*'+URL+'*[/][a-zA-Z0-9/?\[\]()%!+-_]+'
   for aLink in soupHTML.findAll('a'):
      Link = str(aLink.get('href'))
      if re.search(r''+URL,Link):
         potentialLinks.insert(count,Link)
         count+=1
      elif re.match(r'/[a-zA-Z]',Link):
         Link = buildLink(Link,URL)
         potentialLinks.insert(count,Link)
         count+=1

   if len(potentialLinks)<=0:
      return potentialLinks
   reExp =  r'[hH][tT][tT][pP][sS]?://[a-z.+-/]'
   # get all the additional files needed for intended display
   links = soupHTML.findAll('img')
   for link in links:
      if link.get('src'):
         Link = buildLink(link.get('src'),URL)
         if Link:
            rawData = fileRequest(Link)     
            displayID =connection.getID('display')
            query = """INSERT INTO display(displayID,URL,fileType,rawData,pgID)\
                        VALUES(:displayID,:Link,'img',:rawData,:pageID)"""
            connection.query(query,(displayID,Link,rawData,pageID))
   links = soupHTML.findAll('link')
   for link in links:
      if link.get('href'):
         Link = buildLink(link.get('href'),URL)
         if Link:
            rawData = fileRequest(Link)
            displayID = connection.getID('display')
            query = """INSERT INTO display(displayID,URL,fileType,rawData,pgID)\
                        VALUES(:displayID,:Link,'link',:rawData,:pageID)"""
            connection.query(query,(displayID,Link,rawData,pageID))
            
   # get all tags in webpage
   htmlString = soupHTML.prettify()
   lines =  htmlString.split('\n')
   RE = r'\s*<[a-zA-Z0-9\s!-_/=?.\'\"@:\|{}()]+>\s*'
   RED = r'<[a-zA-Z0-9\s!-_/=?.\'\"@:\|{}()]+>'
   count=0
   for line in lines: 
      if re.match(RE,str(line)):
         Retag = re.search(RED,line)
         tag = str(Retag.group())
         tagNo = connection.getID('tags')
         query = """INSERT INTO tags (pageID,tag,tagNo)\
                         VALUES(:pageID,:tag,:tagNo)"""
         
         connection.query(query,(pageID,tag,tagNo))
         contentNo = connection.getID('content')
         query = """INSERT INTO content (pageID,content,contentNo)\
                         VALUES(:pageID,:tag,:contentNo)"""
         connection.query(query,(pageID,tag,tagNo))
      else:
         contentNo = connection.getID('content')
         content = 'content'+str(count)
         query = """INSERT INTO content (pageID,content,contentNo)\
                         VALUES(:pageID,:content,:tagNo)"""
         connection.query(query,(pageID,content,contentNo))
         count+=1

   return potentialLinks
               
               


################################################################################
# Title:         webScraper
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   Provides webscraping functionality to the system
# Arguments:     testID, URL
# Sub-processes: fileRequest, intermediateParser
################################################################################

def webScraper(connection, testID, URL,siteID):
   print("This is the  WebScraper Module")
   print(URL)
   reExp =  r'[hH][tT][tT][pP][sS]?://[a-z.+-]'
   html = fileRequest(URL)
   Stype = 'temp'
   if html:
      print("have html")
      pageID = connection.getID('webpages')
      query = """INSERT INTO webpages (pageID, URL, rawData, siteID) VALUES(:pageID,:URL, :rawData, :siteID)"""
      connection.query(query,(pageID,URL,html,siteID))
      data = intermediateParser(connection,testID,pageID,html,URL)
      return data
   return None




















