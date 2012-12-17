'''
Created on Jan 11, 2012

@author: newatv2user
'''

from VideoHosts import BaseVideoHost, Unique
import re, imp
print 'Inside Ooyala'
try:
    from ooyalalib.utils.Common import Common as CommonUtils
    from ooyalalib.MagicNaming import MagicNaming
    from ooyalalib.ooyalaCrypto import ooyalaCrypto
except:
    print 'Import Error'
    from ooyalalib.utils.Common import Common as CommonUtils
    from ooyalalib.MagicNaming import MagicNaming
    from ooyalalib.ooyalaCrypto import ooyalaCrypto 

class Ooyala(BaseVideoHost):
    '''Media resolver for ooyala'''

    @classmethod
    def match(cls, src):
        '''Returns True if a ooyala video is found embedded in the provided
        src.

        '''
        return ('http://player.ooyala.com/' in src)



    @classmethod
    def resolve(cls, src):
        '''Resolve playable media path for ooyala

        '''
        #swfUrl = "http://player.ooyala.com/static/cacheable/b3898c60dc422629d987a5755bc450e6/player_v2.swf/[[DYNAMIC]]/2"
        #url_ptn = '%s swfVfy=1 app=ondemand?_fcs_host=cp76677.edgefcs.net tcUrl=rtmp://63.97.94.116/ondemand?_fcs_vhos.t=cp76677.edgefcs.net pageUrl=http://documentary.net swfUrl=' + swfUrl
        #url_ptn = '%s app=ondemand?_fcs_host=cp76677.edgefcs.net tcUrl=rtmp://63.97.94.116/ondemand?_fcs_vhos.t=cp76677.edgefcs.net pageUrl=http://documentary.net'
            
        matches = re.findall('embedCode=([^.&"]+)', src)
        
        if matches is None:
            return None
        
        retlist = []
        prevmatch = ''
        for match in Unique(matches):
            if match == prevmatch:
                continue
            embedCode = match
            smil = CommonUtils().grabEncrypted(embedCode)
            decrypted_smil = ooyalaCrypto().ooyalaDecrypt(smil)
            #print decrypted_smil
            videoArray = MagicNaming().getVideoUrl(decrypted_smil)
            #print videoArray
            
            retlist.extend(videoArray)         
            prevmatch = match
        if len(retlist) > 0:
            return retlist    
        return None
