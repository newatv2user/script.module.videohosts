'''
Created on Dec 15, 2011

@author: newatv2user
'''

from VideoHosts import BaseVideoHost, Unique
import re


class YouTube(BaseVideoHost):
    '''Media resolver for http://www.youtube.com'''
    '''altcode = re.compile('href="http://www.youtube.com/view_play_list(.+?)"').findall(link)
    secondaltcode = re.compile('.*src="http://www.youtube.com/embed/videoseries\?list=(.+?)"').findall(link)
    thirdaltcode = re.compile('value="http://www.youtube.com/p/(.+?)"').findall(link)'''
    _patternsPL = [
        ('http://www.youtube.com/embed/videoseries',
         re.compile(r'http://www.youtube.com/embed/videoseries\?list=([^&\?"]+)')),
        ('http://www.youtube.com/p/',
         re.compile(r'http://www.youtube.com/p/([^&\?"]+)')),
        ('http://www.youtube.com/view_play_list',
         re.compile(r'http://www.youtube.com/view_play_list\?=([^&\?"]+)'))          
        ]
    
    _patterns = [
        # (x, y)
        #     x: text pattern to check for existence of a youtube video
        #     y: regular expression that captures the youtube video id in
        #        match.group(1)
        ('http://www.youtube.com/embed/',
         re.compile(r'http://www.youtube.com/embed/([^\?"]+)')),
        ('http://www.youtube.com/v/',
         re.compile(r'http://www.youtube.com/v/([^&\?"]+)')),
        ('http://www.youtube.com/watch',
         re.compile(r'http://www.youtube.com/watch\?v=([^&\?"\'<]+)')),
        ('http://www.youtube-nocookie.com/embed/',
         re.compile(r'http://www.youtube-nocookie.com/embed/([^\?"]+)'))
    ]


    @classmethod
    def match(cls, src):
        '''Returns True if a youtube video is found embedded in the provided
        src.

        '''
        for ptn, _ in cls._patternsPL:
            if ptn in src:
                return True
            
        for ptn, _ in cls._patterns:
            if ptn in src:
                return True
        

    @classmethod
    def resolve(cls, src):
        '''Retuns a playable XBMC media url pointing to the YouTube plugin or
        None.

        '''
        url_ptn = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s'
        url_ptnPL = 'plugin://plugin.video.youtube?action=play_all&playlist=%s'
        retlist = []
        for _, ptn in cls._patternsPL:
            matches1 = ptn.findall(src)
            for match in Unique(matches1):
                #print match
                if match.find('PL', 0, 2) != -1:
                    #print 'found PL'
                    match = match.replace('PL', '')
                print match
                retlist.append(url_ptnPL % match)
        #print src    
        for _, ptn in cls._patterns:
            matches2 = ptn.findall(src)
            for match in Unique(matches2):
                if match == 'videoseries':
                    continue
                retlist.append(url_ptn % match)         
           
        if len(retlist) > 0:
            return retlist 
        return None
        
