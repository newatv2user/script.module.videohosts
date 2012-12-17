'''
Created on Dec 15, 2011

@author: newatv2user
'''

from VideoHosts import BaseVideoHost, _download, Unique
import re


class Stagevu(BaseVideoHost):
    '''Resolver for http://stagevu.com'''


    @classmethod
    def match(cls, src):
        '''Returns True if a stagevu url is found in the page.'''
        return 'http://stagevu.com/' in src


    @classmethod
    def resolve(cls, src):
        '''Returns a media url for a stagevu video found in the provided src.
        Returns None if the media url cannot be resolved.

        '''
        matches = re.findall(
                r'http://stagevu.com/video/([^&\?"]+)', src)
        retlist = []
        for match in Unique(matches):
            retlist.append(cls._get_media_url(
                   'http://stagevu.com/video/%s' % 
                   match))
        if len(retlist) > 0:
            return retlist
        return None


    @classmethod
    def _get_media_url(cls, url):
        '''Returns the the media url for a given stagevu video URL or None.'''
        #print url
        match = re.search(r'<param name="src" value="(.+?)"', _download(url))
        if match:
            return ('%s'
                    % match.group(1))
        return None
        
