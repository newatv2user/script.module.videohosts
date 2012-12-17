'''
Created on Dec 15, 2011

@author: newatv2user
'''

from VideoHosts import BaseVideoHost, _download, Unique
import re


class VeeHD(BaseVideoHost):
    '''Resolver for http://veehd.com'''

    _patterns = [
        # (x, y)
        #     x: text pattern to check for existence of a veehd video
        #     y: regular expression that captures the veehd video id in
        #        match.group(1)
        ('http://veehd.com/vpi',
         re.compile(r'<embed type="video/divx" src="([^"]+)')),
        ('http://veehd.com/vpi',
         re.compile(r'"url":"(http[^"]+)')),
    ]
    
    @classmethod
    def match(cls, src):
        '''Searches for the veehd URL'''
        return ('http://veehd.com/video/' in src)


    @classmethod
    def resolve(cls, src):
        '''Returns a media url for a veehd video found in the provided src.
        Returns None if the media url cannot be resolved.

        '''
        matches = re.findall(
                r'http://veehd.com/video/([^&\?",/]+)', src)
        retlist = []
        for match in Unique(matches):
            retlist.append(cls._get_media_url(
                   'http://veehd.com/video/%s' % 
                   match))
            
        if len(retlist) > 0:
            return retlist
        return None


    @classmethod
    def _get_media_url(cls, url):
        '''Returns the the media url for a given veehd video URL or None.'''
        #print url
        match = re.search(r'(/vpi\?h=.+?do=s.+?)"', _download(url))
        if match:
            match2 = 'http://veehd.com' + match.group(1)
            #print match2
            src2 = _download(match2)
            #print src2
            for _, ptn in cls._patterns:
                match = ptn.search(src2)
                if match:
                    return ('%s' % match.group(1))
                #else:
                #    print str(ptn) + ' Match not found.'
            '''newmatch = re.search(r'<embed type="video/divx" src="([^&"]+)"', _download(match2))
            if newmatch:
                return ('%s'
                    % newmatch.group(1))'''
        return None
        
