'''
Created on Jan 18, 2013

@author: newatv2user
'''

from VideoHosts import BaseVideoHost, Unique
import re
import urllib2
import CommonFunctions

# For parsedom
common = CommonFunctions
common.dbg = False
common.dbglevel = 3


class Movshare(BaseVideoHost):
    '''Media resolver for Movshare'''
    _patterns = [
        # (x, y)
        #     x: text pattern to check for existence of a dailymotion video
        #     y: regular expression that captures the dailymotion video id in
        #        match.group(1)
        ('http://www.movshare.net/video/', re.compile(r'http://www.movshare.net/video/([^\?&"]+)')),
        ('http://embed.movshare.net/embed.php', re.compile(r'http://embed.movshare.net/embed.php\?v=([^&"]+)'))
    ]


    @classmethod
    def match(cls, src):
        '''Returns True if a movshare video is found embedded in the provided
        src.

        '''
        for ptn, _ in cls._patterns:
            if ptn in src:
                #print 'match found'
                return True
            
        return False



    @classmethod
    def resolve(cls, src):
        '''Retuns a playable XBMC media url.
        '''
        #print 'In Movshare: resolve'
        url_ptn = 'http://www.movshare.net/video/%s'
        
        retlist = []
        for _, ptn in cls._patterns:
            #print ptn
            #print src
            matches = ptn.findall(src)
            #print 'Num of pattern matches: ' + str(len(matches2))
            for match in Unique(matches):
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
        '''Returns the the media url for a given movshare video URL or None.'''
        #print 'resolving link for ' + url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        #print 'resolving link step 2'
        html = response.read()
        response.close()
        
        if re.search(r'Video hosting is expensive. We need you to prove you\'re human.', html):
            resp = urllib2.urlopen(req)
            html = resp.read()
            resp.close()
        
        # From AJ turtle code
        video_info_link = re.compile('<embed type="video/divx" src="(.+?)"').findall(html)
        video_link = None
        if len(video_info_link) == 0:
            domainStr = re.compile('flashvars.domain="(.+?)"').findall(html)[0]
            fileStr = re.compile('flashvars.file="(.+?)"').findall(html)[0]
            filekeyStr = re.compile('flashvars.filekey="(.+?)"').findall(html)[0]
            
            video_info_link = domainStr + '/api/player.api.php?user=undefined&pass=undefined&codes=1&file=' + fileStr + '&key=' + filekeyStr
            req = urllib2.Request(video_info_link)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
            res = urllib2.urlopen(req)
            html = res.read()
            res.close()
            video_link = re.compile(r'url=(.+?)&').findall(html)[0]
        else:
            video_link = video_info_link[0]

        return video_link
