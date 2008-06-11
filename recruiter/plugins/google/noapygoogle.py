import urllib2
import re

import spellingSuggestions

filters = { "use+share" : "(cc_publicdomain%7Ccc_attribute%7Ccc_sharealike%7Ccc_noncommercial%7Ccc_nonderived)",
            "use+share+comm" : "(cc_publicdomain%7Ccc_attribute%7Ccc_sharealike%7Ccc_nonderived).-(cc_noncommercial)",
            "use+share+modif"    : "(cc_publicdomain%7Ccc_attribute%7Ccc_sharealike%7Ccc_noncommercial).-(cc_nonderived)",
            "use+share+modif+comm" : "(cc_publicdomain%7Ccc_attribute%7Ccc_sharealike).-(cc_noncommercial%7Ccc_nonderived)"}

defHeaders = { 
'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv \u2014 1.7.8) Gecko/20050511'
            }

regex = re.compile(r'<div class=g><!--m--><h2 class=r>'
                   +'<a href=\"(.*?)\" class=l>(.*?)</a>.*?<div class=std>'
                   +'(.*?)<br><span class=a>', re.DOTALL)
        
def setProxy( proxy ):
    
    proxyHandler = urllib2.ProxyHandler({ "http" : "http://" 
                                         + proxy[user] + ":" 
                                         + proxy[passwd] + "@" 
                                         + proxy[host] + ":" 
                                         + proxy[port]
                                         })
    
    proxyOpener = urllib2.build_opener( proxyHandler, urllib2.HTTPHandler )

    urllib2.install_opener( proxyOpener )
   
def createReq( url, headers, proxy ):
    global dedfHeaders
    
    req = urllib2.Request( url )
    
    if headers:
        defHeaders.update(headers)
    if proxy: 
        pass
    
    for header in defHeaders:
        req.add_header( header, defHeaders[header])
    
    return req
    
def search( q, start = 0, maxResults = 10, filter = '',
                    restrict = '', safeSearch = 'images', 
                    language = '', headers = None, 
                    http_proxy = None ):
    '''
    Search Google using urllib2 and returns the results
    
    This function will executre the google search and then will return
    the results to the user, but first it will parse the search executed.
    
    
    @param q: search string.  
    @type  q: String

    @param start: (optional) zero-based index of first desired result.
    @type  start: int

    @param maxResults: (optional) maximum number of results to return.
    @type  maxResults: int

    @param filter: (optional) flag to request filtering of similar results
    @type  filter: int

    @param restrict: (optional) restrict results by country or topic.
    @type  restrict: String    

    @param safeSearch: (optional)
    @type  safeSearch: int

    @param language: (optional)
    @type  language: String

    @param http_proxy: (optional) the HTTP proxy to use for talking to Google
    @type  http_proxy: String
    
    @return: the search results
    '''
    
    global regex
    
    if filter:
        filter = filters[filter]
        
    if not safeSearch == "images": 
        safeSearch = "active"
    
    url = "http://www.google.com/search?as_q=" + q \
            + "&hl="  + language   \
            + "&num=" + str(maxResults) \
            + "&as_rights=" + filter \
            + "&safe=" + safeSearch
 
    req = createReq( url, headers, http_proxy )
    
    try:
        search = urllib2.urlopen( req ).read()
        
        matches = (regex.findall( search ))[start:] 
        
        toreturn = []
        
        for x in range(len(matches)):
            temp = { 'link' : matches[x][0],
                     'title' : matches[x][1],
                     'description' : matches[x][2] }
            
            toreturn.append(temp)
            
        object = {"matches" : len(toreturn), 
                  "results" : toreturn }
    
        print object
        return object
    
    except urllib2.HTTPError, e:
        
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
        
    except urllib2.URLError, e:
        
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
        
def translateWord( word, langpair, headers = None, http_proxy = None):
    
    url = "http://translate.google.com/translate_dict" \
            + "?q=" + word \
            + "&hl=es&langpair=" + langpair
    
    req = createReq( url, headers, http_proxy )
    
    return spellingSuggestions.wordSpell( req )
    