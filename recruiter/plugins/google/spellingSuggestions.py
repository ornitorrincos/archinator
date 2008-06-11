import urllib2
import re

regex = re.compile(r'<span class=\"definition\">(.*?)<span class=\"comment\">(.*?)</span><span class=\"grammar_code\">(.*?)</span>',re.DOTALL)

def wordSpell( req ):
    global regex
    
    try:
        search = urllib2.urlopen( req ).read()
        matches = (regex.findall( search )) 
        
        toreturn = []
        
        for x in range(len(matches)):
            temp = { 'definition'   : matches[x][0],
                     'comment'      : matches[x][1],
                     'grammar_code' : matches[x][2] }
            
            toreturn.append(temp)
            
        object = {"matches" : len(toreturn), 
                  "results" : toreturn }
    
        return object
    
    except urllib2.HTTPError, e:
        
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
        
    except urllib2.URLError, e:
        
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason