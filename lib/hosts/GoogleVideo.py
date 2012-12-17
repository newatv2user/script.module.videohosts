'''
Created on Dec 15, 2011

@author: newatv2user
'''

from VideoHosts import BaseVideoHost, _unhex, _download, Unique
import re
import urllib
from cgi import parse_qs


class GoogleVideo(BaseVideoHost):
    '''Media resolver for http://video.google.com'''


    @classmethod
    def match(cls, src):
        '''Returns True if a google video url is found in the page.'''
        return 'http://video.google.com' in src


    @classmethod
    def resolve(cls, src):
        '''Returns a media url for a google video found in the provided src.
        Returns None if the media url cannot be resolved.

        '''
        matches = re.findall(
                r'http://video.google.com/googleplayer.swf\?docId=(.+?)"', src)
        retlist = []
        for match in Unique(matches):
            retlist.append(cls._get_media_url(
                   'http://video.google.com/videoplay?docid=%s' % 
                   match))
            
        if len(retlist) > 0:
            return retlist
        return None


    @classmethod
    def _get_media_url(cls, url):
        print url
        '''Returns the the media url for a given google video URL or None.'''
        flvurl_match = re.search(r'preview_url:\'(.+?)\'', _download(url))
        if not flvurl_match:
            return None

        flvurl = _unhex(flvurl_match.group(1))
        params = parse_qs(flvurl.split('?', 1)[1])
        return urllib.unquote_plus(params['videoUrl'][0])
        
        
