'''
Created on Feb 13, 2012

@author: Vaio
'''

from VideoHosts import BaseVideoHost, Unique
import re
import urllib2
import CommonFunctions

# For parsedom
common = CommonFunctions
common.dbg = False
common.dbglevel = 3


class Dailymotion(BaseVideoHost):
    '''Media resolver for Dailymotion'''
    _patternsPL = [
        ('http://www.dailymotion.com/widget/jukebox?list[]=',
         re.compile(r'http://www\.dailymotion\.com/widget/jukebox\?list\[]=%2Fplaylist%2F([^/%&"]+)')),
        ('http://www.dailymotion.com/playlist/',
         re.compile(r'http://www\.dailymotion\.com/playlist/([^/%&"]+)'))        
        ]
    
    _patterns = [
        # (x, y)
        #     x: text pattern to check for existence of a dailymotion video
        #     y: regular expression that captures the dailymotion video id in
        #        match.group(1)
        ('http://www.dailymotion.com/swf/video/', re.compile(r'http://www.dailymotion.com/swf/video/([^\?&"]+)')),
        ('http://www.dailymotion.com/embed/video/', re.compile(r'http://www.dailymotion.com/embed/video/([^\?&"]+)')),
        ('http://www.dailymotion.com/video/', re.compile(r'http://www.dailymotion.com/video/([^\?&"><\']+)'))
    ]


    @classmethod
    def match(cls, src):
        '''Returns True if a dailymotion video is found embedded in the provided
        src.

        '''
        #print 'In Dailymotion: match'
        #print src
        for ptn, _ in cls._patternsPL:
            if ptn in src:
                #print 'match found PL'
                return True
            
        for ptn, _ in cls._patterns:
            if ptn in src:
                #print 'match found'
                return True
            
        return False



    @classmethod
    def resolve(cls, src):
        '''Retuns a playable XBMC media url.
        '''
        #print 'In Dailymotion: resolve'
        url_ptn = 'http://www.dailymotion.com/video/%s'
        url_ptn2 = 'http://www.dailymotion.com%s'
        #url_ptnPL = 'plugin://plugin.video.youtube?action=play_all&playlist=%s'
        retlist = []
        for _, ptn in cls._patternsPL:
            matches1 = ptn.findall(src)
            for match in Unique(matches1):
                PLurl = 'http://www.dailymotion.com/playlist/' + match
                req = urllib2.Request(PLurl)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req)
                link = response.read()
                response.close()
                
                PLItems = re.compile('class="dmco_simplelink.* href="(/video/.+?)"').findall(link)
                for PLItem in Unique(PLItems):
                    #print PLItem
                    itemurl = url_ptn2 % PLItem
                    vidurl = cls._get_media_url(itemurl)
                    if vidurl:
                        retlist.append(vidurl)
            
        for _, ptn in cls._patterns:
            #print ptn
            #print src
            matches2 = ptn.findall(src)
            #print 'Num of pattern matches: ' + str(len(matches2))
            for match in Unique(matches2):
                #print 'match found: ' + match
                #if match == 'videoseries':
                #    continue
                itemurl = url_ptn % match
                vidurl = cls._get_media_url(itemurl)
                #print vidurl
                if vidurl:
                    retlist.append(vidurl)         
           
        if len(retlist) > 0:
            return retlist 
        return None
        
    @classmethod
    def _get_media_url(cls, url):
        '''Returns the the media url for a given dailymotion video URL or None.'''
        #print 'resolving link for ' + url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        #print 'resolving link step 2'
        link = response.read()
        response.close()
        #sequence = re.compile('"sequence",  "(.+?)"').findall(link)
        link = link.replace('\r\n', '').replace('\r', '').replace('\n', '')
        #print link
        #sequence = None
        sequence = re.compile('"sequence":"(.+?)"').findall(link)
        #print 'resolving link step 3'
        if not sequence:            
            print 'reg ex failure' 
            return None
                
        newseqeunce = urllib2.unquote(sequence[0]).decode('utf8').replace('\\/', '/')
        
        dm_low = re.compile('"sdURL":"(.+?)"').findall(newseqeunce)
        dm_high = re.compile('"hqURL":"(.+?)"').findall(newseqeunce)
        videoUrl = None
        
        if dm_high is None or len(dm_high) == 0:
            videoUrl = dm_low[0]
        else:
            videoUrl = dm_high[0]
                        
        if videoUrl:
            return videoUrl
        return None
