import os
import sys
import pandas as pd 
import numpy as np
import re

#--------------------------------------------------------
def getMonthPages():

    #Run
    for i in range(2011,2021):
        for j in range(12):
            year = str(i)
            month = str(j+1).zfill(2)
            savename = '../data/months/page_' + year + '_' + month + '.html'
            urlname = 'http://podcast.hernancattaneo.com/' + year + '/' + month + '/'
            cmd = 'wget --quiet -O ' + savename + ' ' + urlname
            os.system(cmd)

#--------------------------------------------------------
def getEpisodes():

    #Get HTML pages
    myurls = []
    for root, dirs, files in os.walk("../data/months/", topdown=False):
        for name in files:
            if 'html' in name:
                myurls.append(os.path.join(root, name))    
    myurls = np.sort(myurls)

    #Open and find links
    for page in myurls:

        #Open and read
        mylines = []
        with open(page,'r') as f:
            for line in f:
                mylines.append(line)

        #Process if not empty        
        if (len(mylines) > 0):
            starts = []
            for l,line in enumerate(mylines):
                if '<div class="post">' in line:
                    starts.append(l)        
            for start in starts:
                refline = mylines[start+1]
                index = refline.index("href")
                refline = refline[index:]
                index = refline.index('bookmark')
                refline = refline[8:index-7]
                if 'starting-on' not in refline:
                    elements = refline.split('/')
                    savename = '../data/episodes/' + elements[-2] + '.html'
                    cmd = 'wget --quiet -O ' + savename + ' ' + refline
                    os.system(cmd)

#--------------------------------------------------------
def download():

    #Get HTML pages
    myurls = []
    for root, dirs, files in os.walk("../data/episodes/", topdown=False):
        for name in files:
            if 'html' in name:
                myurls.append(os.path.join(root, name))    
    myurls = np.sort(myurls)
    
    #Get Download Link
    count = 0
    for m,myurl in enumerate(myurls):

        #Open and read
        count = count + 1
        mylines = []
        with open(myurl,'r') as f:
            for line in f:
                mylines.append(line)

        #Get Link
        for m,myline in enumerate(mylines):
            if '<div class="entrytext">' in myline:
                tracks = ' '.join(mylines[m:m+20])
                tracks = tracks.replace('&amp;','and')
                tracks = tracks.replace(' /','')
                tracks = tracks.replace('Download episode on MP3 (Right click, save link as...)','')
                match = re.findall(r'\>(.*?)\<',tracks)
                match = [item for item in match if len(item) > 0]
                match = [item for item in match if item != ' ']
                match = [item for item in match if '\t' not in item]
                match = [item for item in match if 'Share' != item]
                match = [item for item in match if 'Loading' != item]
                match = [item for item in match if 'Download' != item]
                match = [item for item in match if ' tracklist' not in item.lower()]
                match = [item for item in match if '(' != item]
                match = [item for item in match if ')' != item]
                match = [item for item in match if ' | ' != item]
                tracklist = '| '.join(match)
            if 'data-uri="' in myline:
                index = myline.index('data-uri="')
                myline = myline[index:]
                index = myline.index('<iframe')
                myline = myline[10:index-3]
                elements = myline.split('/')
                savename = '/Volumes/2TStorage/Podcasts/hernan_cattaneo/' + elements[-1]
                with open('../data/tracklist/tracklist.txt','a') as f:
                    f.write(str(m) + ',' + elements[-1] + ',' + tracklist + '\n')
                #cmd = 'wget -O ' + savename + ' ' + myline
                #os.system(cmd)



#--------------------------------------------------------
if __name__ == '__main__':

    #Clear
    os.system('clear')

    #Get Month Pages
    #getMonthPages()
    
    #Find Links in Month Pages
    #getEpisodes()

    #Get Download Links
    download()
