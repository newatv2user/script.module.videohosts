'''
Created on Dec 15, 2011

@author: newatv2user
'''

from VideoHosts import BaseVideoHost, _download, Unique
import re


class NatGeo(BaseVideoHost):
    '''Resolver for National Geographic'''


    @classmethod
    def match(cls, src):
        '''Returns True if a nat geo url is found in the page.'''
        return 'http://video.nationalgeographic.com/' in src


    @classmethod
    def resolve(cls, src):
        '''Returns a media url for a natgeo video found in the provided src.
        Returns None if the media url cannot be resolved.

        '''
        matches = re.findall(
                r'(http://video.nationalgeographic.com/[^"&;=]+?.smil)', src)
        retlist = []
        for match in Unique(matches):
            retlist.append(cls._get_media_url(match))
        if len(retlist) > 0:
            return retlist
        return None


    @classmethod
    def _get_media_url(cls, url):
        '''Returns the the media url for a given natgeo video URL or None.'''
        #print url
        link = _download(url)
        content = re.compile('content="([^"]+)"').findall(link)
        if content:
            content = content[0]
        else:
            return None
        
        src = re.compile('src="([^"]+)"').findall(link)
        if src:
            src = src[0]
        else:
            return None
        
        return content + src