'''
Created on Dec 15, 2011

@author: newatv2user

Based on the original videohost concept by jbel
'''

#import urllib
#from inspect import isclass
#from collections import defaultdict
import pkgutil
import imp, sys, os

#__all__ = ["YouTube", "GoogleVideo", "Vimeo"]


def resolve(src):
    '''Attempts to return a media url for the given page's source.

    First loops through all available hosts stopping at the first host that
    returns True when HOST.match(src) is called. Then host.resolve(src) is
    called to compute the actual media url.

    '''
    #print 'In resolve '
    ## walk_packages vs iter_modules???
    retlist = []
    for _, name, _ in pkgutil.iter_modules(__path__):
    #for _, name, _ in pkgutil.walk_packages(path=['lib']):
    #for name in __all__:
        
        #print 'In hosts: ' + name

        # VideoHosts is a base class, so skip
        if name == "VideoHosts" or name == "ooyalalib":
            continue
        path = os.path.dirname(os.path.abspath(__file__))
        #print "In path:", path in sys.path
        sys.path.append(path)
        info = imp.find_module(name, __path__)
        if info is None:
            print 'Is it a valid module: ' + name
            continue
        #print info[0]
        #print info[1]
        #print info[2]
        try:
            #path = __path__
            
            #module = __import__(name)
            #print "Imported", module
            test = imp.load_module(name, *info)
            klass = getattr(test, name)
        except ImportError:
            #print str(ImportError.message)
            print "Could not import"
            #return "Could not import module"
            continue
            #pass
        finally:
            pass
            #print 'closing file'
            #info[0].close()
        if klass.match(src):
            resList = klass.resolve(src)
            if resList is not None:
                retlist.extend(resList)
        
    return retlist
