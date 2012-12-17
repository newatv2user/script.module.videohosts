'''
Created on Dec 15, 2011

@author: newatv2user
'''

from VideoHosts import BaseVideoHost, Unique
import re


class PBS(BaseVideoHost):
    '''Resolver for http://pbs.org'''


    @classmethod
    def match(cls, src):
        '''Searches for the pbs video embedded iframe url.'''
        return ('PBSPlayer.swf' in src)


    @classmethod
    def resolve(cls, src):
        '''Extracts a vimeo video id from the source and returns a playable
        XBMC URL to the Vimeo plugin.

        '''
        matches1 = re.findall(r'name="flashvars" value="video=(.+?)&',
                          src)
        retlist = []
        for match in Unique(matches1):
            retlist.append('plugin://plugin.video.pbs/?play=%s'
                    % match)
            
        if len(retlist) > 0:
            return retlist
        return None
        
