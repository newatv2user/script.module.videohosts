'''
Created on Dec 15, 2011

@author: newatv2user

Based on the original videohost concept by jbel
'''

import urllib
#from inspect import isclass
#from collections import defaultdict


class BaseVideoHost(object):
    '''Abstract base class for video host resolvers. Subclasses must override
    the match and resolve methods and should be callable as @classmethods.

    '''

    @classmethod
    def match(cls, src):
        '''Return True or False if cls is able to resolve a media url for the
        given src.

        '''
        raise NotImplementedError

    @classmethod
    def resolve(cls, src):
        '''Return a media url or None for the given src.'''
        raise NotImplementedError

        
def _download(url):
    '''Returns the response from the GET request for a given url.'''
    conn = urllib.urlopen(url)
    resp = conn.read()
    conn.close()
    return resp


# _unhex modeled after python's urllib.unquote
_hextochr = dict(('%02x' % i, chr(i)) for i in range(256))
_hextochr.update(('%02X' % i, chr(i)) for i in range(256))


def _unhex(inp):
    '''Returns a new string, unescaping any instances of hex encoded
    characters.

    >>> _unhex(r'abc\x20def')
    'abc def'

    '''
    res = inp.split(r'\x')
    for i in xrange(1, len(res)):
        item = res[i]
        try:
            res[i] = _hextochr[item[:2]] + item[2:]
        except KeyError:
            res[i] = '%' + item
        except UnicodeDecodeError:
            res[i] = unichr(int(item[:2], 16)) + item[2:]
    return ''.join(res)


# Populate the list of available video hosts to match against. Get any class
# that is a subclass of BaseVideoHost but do not include BaseVideoHost itself!

'''AVAILABLE_HOSTS = [attr_value for attr_name, attr_value in locals().items()
                   if isclass(attr_value) and attr_name != 'BaseVideoHost' and
                   issubclass(attr_value, BaseVideoHost)]
'''

"""def resolve(src):
    '''Attempts to return a media url for the given page's source.

    First loops through all available hosts stopping at the first host that
    returns True when HOST.match(src) is called. Then host.resolve(src) is
    called to compute the actual media url.

    '''
    #print str(inheritors(BaseVideoHost))
    '''for host in AVAILABLE_HOSTS:
        if host.match(src):
            return host.resolve(src)
    return None'''
"""

def Unique(seq, idfun=None):
    ''' Return a unique list
        Source: http://www.peterbe.com/plog/uniqifiers-benchmark
    '''
    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result
