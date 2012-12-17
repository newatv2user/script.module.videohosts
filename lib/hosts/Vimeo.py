'''
Created on Dec 15, 2011

@author: newatv2user
'''

from VideoHosts import BaseVideoHost, Unique
import re


class Vimeo(BaseVideoHost):
    '''Resolver for http://vimeo.com'''


    @classmethod
    def match(cls, src):
        '''Searches for the vimeo swf URL or finds an embedded iframe url.'''
        return ('http://vimeo.com/moogaloop.swf' in src or
                'http://player.vimeo.com/video/' in src)


    @classmethod
    def resolve(cls, src):
        '''Extracts a vimeo video id from the source and returns a playable
        XBMC URL to the Vimeo plugin.

        '''
        matches1 = re.findall(r'http://vimeo.com/moogaloop.swf\?clip_id=(.+?)&',
                          src)
        retlist = []
        for match in Unique(matches1):
            retlist.append('plugin://plugin.video.vimeo/?action=play_video&videoid=%s'
                    % match)
        
        matches2 = re.findall('http://player.vimeo.com/video/(.+?)"', src)
        for match in Unique(matches2):
            retlist.append('plugin://plugin.video.vimeo/?action=play_video&videoid=%s'
                    % match)
            
        if len(retlist) > 0:
            return retlist
        return None
        
