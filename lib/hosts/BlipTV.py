'''
Created on Dec 15, 2011

@author: newatv2user
'''

from VideoHosts import BaseVideoHost, Unique
import re
import urllib2

class BlipTV(BaseVideoHost):
    '''Media resolver for http://www.youtube.com'''

    @classmethod
    def match(cls, src):
        '''Returns True if a bliptv video is found embedded in the provided
        src.

        '''
        return ('http://blip.tv/play' in src)



    @classmethod
    def resolve(cls, src):
        '''Retuns a playable XBMC media url pointing to the Bliptv plugin or
        None.

        '''
        url_ptn = 'plugin://plugin.video.bliptv/?action=play_video&videoid=%s'
        matches = re.findall('(http://blip.tv/play/[^.&"]+)', src)
        
        retlist = []
        for match in Unique(matches):
            videoId = cls._get_media_url(match)
            if videoId:
                retlist.append(url_ptn % videoId)         
            
        if len(retlist) > 0:
            return retlist    
        return None

    @classmethod
    def _get_media_url(cls, url):
        '''Get video Id and return blip tv plugin url.'''
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        gurl = response.geturl()
        videoID = re.compile('rss%2Fflash%2F([^&%]+)').findall(gurl)
        if videoID:
            #print videoID[0]
            return videoID[0]
        return None