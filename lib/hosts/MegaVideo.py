'''
Created on Dec 15, 2011

@author: newatv2user
'''

from VideoHosts import BaseVideoHost, Unique
import re
import urllib2


class MegaVideo(BaseVideoHost):
    '''Resolver for http://megavideo.com'''


    @classmethod
    def match(cls, src):
        '''Searches for the megavideo url.'''
        return ('http://www.megavideo.com/v/' in src)


    @classmethod
    def resolve(cls, src):
        ''' Get a playable megavideo link

        '''
        matches = re.findall(r'(http://www.megavideo.com/v/[^"]+)',
                          src)
        
        retlist = []
        for match in Unique(matches):
            movielink = cls._get_media_url(match)
            if movielink:
                #return ('%s' % movielink)
                retlist.append(movielink)
                
        if len(retlist) > 0:
            return retlist
        return None

    @classmethod
    def _get_media_url(cls, url):
        '''Returns the the media url for a given stagevu video URL or None.'''
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        gurl = response.geturl()
        #print str(gurl)
        codemegahack = re.compile('&v=([^&"/]+)').findall(gurl)
        #codemega = gurl[-8:]
        codemega = codemegahack[0]
        #print str(codemega)
        req = urllib2.Request("http://www.megavideo.com/xml/videolink2.php?v=" + codemega)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        req.add_header('Referer', 'http://www.megavideo.com/')
        lemon = urllib2.urlopen(req);response = lemon.read();lemon.close()
        errort = re.compile(' errortext="(.+?)"').findall(response)
        
        movielink = ''
        if len(errort) == 0:
            s = re.compile(' s="(.+?)"').findall(response)
            k1 = re.compile(' k1="(.+?)"').findall(response)
            k2 = re.compile(' k2="(.+?)"').findall(response)
            un = re.compile(' un="(.+?)"').findall(response)
            #print str(s[0]) + ' ' + str(un[0]) + ' ' + str(k1[0]) + ' ' + str(k2[0])
            movielink = 'http://www' + s[0] + '.megavideo.com/files/' + calculateFileHash(un[0], k1[0], k2[0]) + '/?.flv' # Do we need the /?.flv
        
        if movielink:
            return movielink
        return None
        
def calculateFileHash(str1, key1, key2):
    # explode hex to bin strings, collapse to a string and return char array
    chash = explodeBin(str1)
    # based on the keys, generate an array of 384 (256 + 128) values
    decriptIndices = computeIndices(key1, key2)
    # from 256 to 0, swap hash[decriptIndices[x]] with hash[__reg3 % 128]
    chash = doDecriptionSwaps(chash, decriptIndices)
    # replace the first 128 chars in hash with the formula:
    #  hash[x] = hash[x] * decriptIndices[x+256] & 1
    chash = calcDecriptionMix(chash, decriptIndices)
    # split __reg12 in chunks of 4 chars
    chunks = doDecriptionChunks(chash)  
    # convert each binary chunk to a hex string for the final hash
    return toHexDecriptionString(chunks)

def explodeBin(str1):
    # explode each char in str1 into it;s binary representation
    # and collect the result into __reg1
    __reg1 = []
    __reg3 = 0
    while (__reg3 < len(str1)):
        __reg0 = str1[__reg3]
        holder = __reg0
        if (holder == "0"):
            __reg1.append("0000")
        else:
            if (__reg0 == "1"):
                __reg1.append("0001")
            else:
                if (__reg0 == "2"): 
                    __reg1.append("0010")
                else: 
                    if (__reg0 == "3"):
                        __reg1.append("0011")
                    else: 
                        if (__reg0 == "4"):
                            __reg1.append("0100")
                        else: 
                            if (__reg0 == "5"):
                                __reg1.append("0101")
                            else: 
                                if (__reg0 == "6"):
                                    __reg1.append("0110")
                                else: 
                                    if (__reg0 == "7"):
                                        __reg1.append("0111")
                                    else: 
                                        if (__reg0 == "8"):
                                            __reg1.append("1000")
                                        else: 
                                            if (__reg0 == "9"):
                                                __reg1.append("1001")
                                            else: 
                                                if (__reg0 == "a"):
                                                    __reg1.append("1010")
                                                else: 
                                                    if (__reg0 == "b"):
                                                        __reg1.append("1011")
                                                    else: 
                                                        if (__reg0 == "c"):
                                                            __reg1.append("1100")
                                                        else: 
                                                            if (__reg0 == "d"):
                                                                __reg1.append("1101")
                                                            else: 
                                                                if (__reg0 == "e"):
                                                                    __reg1.append("1110")
                                                                else: 
                                                                    if (__reg0 == "f"):
                                                                        __reg1.append("1111")

        __reg3 = __reg3 + 1
    return list("".join(__reg1))

def computeIndices(key1, key2):
    """Generate an array of 384 indices with values 0-127
    @param key1: first seed to generate indices from
    @param key2: second seed to generate indices from
    @return: an array of 384 indices with values between 0 and 127"""
    indices = []
    for _ in range(384):
        key1 = (int(key1) * 11 + 77213) % 81371
        key2 = (int(key2) * 17 + 92717) % 192811
        indices.append((int(key1) + int(key2)) % 128)
    return indices


def doDecriptionSwaps(chash, keys):
    """Swap the first 256 indices from keys on the hash with the last 128 elements from the hash
    @param chash: the hash to do swaps on
    @param keys: the generated keys to use as indices for the swaps
    @return: hash after swaps"""
    for index in range(256, 0, -1):
        key = keys[index]
        swapTarget = index % 128
        oldHashKey = chash[key]
        chash[key] = chash[swapTarget]
        chash[swapTarget] = oldHashKey
    return chash

def calcDecriptionMix(chash, keyMix):
    """Mixes the decription keys into the hash and returns the updated hash
    @param chash: the hash to merge the keys into
    @param keyMix: the array of keys to mix"""
    for i in range(128):
        chash[i] = str(int(chash[i]) ^ int(keyMix[i + 256]) & 1)
    return "".join(chash)


def doDecriptionChunks(binaryMergedString):
    """Break a string of 0's and 1's in pieces of 4 chars
    @param binaryMergedString: a string of 0's and 1's to break in 4-part pieces
    @return: an array of 4 character parts of the original string"""
    binaryChunks = []
    for index in range(0, len(binaryMergedString), 4):
        binaryChunk = binaryMergedString[index:index + 4]
        binaryChunks.append(binaryChunk)
    return binaryChunks

def toHexDecriptionString(binaryChunks):
    """Converts an array of binary strings into a string of the corresponding hex chunks merged
    This method will first loop through the binary strings converting each one into it's correspondent
    hexadecimal string and then merge the resulting array into a string
    @param binaryChunks: an array of binary strings
    @return: a string of the corresponding hexadecimal strings, merged"""
    hexChunks = []
    for binChunk in binaryChunks:
        hexChunks.append("%x" % int(binChunk, 2))    
    return "".join(hexChunks)
