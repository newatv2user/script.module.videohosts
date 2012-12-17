'''
Created on Dec 15, 2011

@author: newatv2user
'''

from VideoHosts import BaseVideoHost, _download, Unique
import re


class HostingBulk(BaseVideoHost):
    '''Resolver for http://hostingbulk.com'''


    @classmethod
    def match(cls, src):
        '''Returns True if a hostingbulk url is found in the page.'''
        return 'http://hostingbulk.com/' in src


    @classmethod
    def resolve(cls, src):
        '''Returns a media url for a hostingbulk video found in the provided src.
        Returns None if the media url cannot be resolved.

        '''
        matches = re.findall(
                r'(http://hostingbulk.com/[^"]+)', src)
        retlist = []
        for match in Unique(matches):
            retlist.append(cls._get_media_url(match))
        if len(retlist) > 0:
            return retlist
        return None


    @classmethod
    def _get_media_url(cls, url):
        '''Returns the the media url for a given hostingbulk video URL or None.'''
        #print url
        link = _download(url)
        # Looks like website has changed. Oct 05, 2012
        videoUrl = re.compile("'file': '([^']+)'").findall(link)
        if videoUrl:
            videoUrl = videoUrl[0]
        return videoUrl
        '''webLink = ''.join(link.splitlines()).replace('\t', '')
        #Trying to find out easy way out :)
        paramSet = re.compile("return p\}\(\'(.+?)\',36,(.+?),\'(.+?)\'").findall(webLink)
                
        result = parseValue(paramSet[0][0], 36, int(paramSet[0][1]), paramSet[0][2].split('|'))
        result = result.replace('\\', '').replace('"', '\'')
        #print result

        #imgUrl = re.compile("s1.addVariable\(\'image\',\'(.+?)\'\);").findall(result)[0]
        videoUrl = re.compile("s1.addVariable\(\'file\',\'(.+?)\'\);").findall(result)[0]
        
        return videoUrl'''
        
# Parse p,a,c,k,e,d string for video URL
def parseValue(p, a, c, k):
        while(c >= 1):
                c = c - 1
                if(k[c]):
                        #p=p.replace(new RegExp('\\b'+c.toString(a)+'\\b','g'),k[c]);
                        base36Str = base36encode(c)
                        p = re.sub('\\b' + base36Str + '\\b', k[c], p)
                        #print k[c] + 'BASE ' + base36Str + 'CONTENT ' + p
        return p
    
def base36encode(number):
        if not isinstance(number, (int, long)):
                raise TypeError('number must be an integer')
        if number < 0:
                raise ValueError('number must be positive')

        alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'

        base36 = ''
        while number:
                number, i = divmod(number, 36)
                base36 = alphabet[i] + base36

        return base36 or alphabet[0]