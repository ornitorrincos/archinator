# -*- coding: utf-8 -*-

import re
import urllib
import feedparser
import database

repos = ["core", "extra", "community"]

class main:
    
    def __init__( self, bot ):
        self.bot = ""
        self.actions = {'archnews'   : self.archnews,
                        'archlinks'   : self.giveLinks,
                        'pksearch'   : self.pkSearch,
                        'pkinfo'     : self.pkInfo }
    
    def archnews( self, *args ):
        news = feedparser.parse("http://www.archlinux.org/feeds/news/")
        news = [ new['title'] for new in news['items'] if 'title' in new ]
        news = (" || ").join(news[:10])
        self.bot.sendtext(news, True)


    def pkInfo( self, package):

        try: 
            html = urllib.urlopen('http://aur.archlinux.org/packages.php?O=0&L=0&C=0&K=' +
                              package + '&SB=n&SO=d&PP=100&SeB=nd&do_Orphans=').read()
        except URLError, e:
            self.bot.sendtext("The url couldn't be reached", True)
            
                               
        found = re.search('packages.php\?ID=(.*?)\'.*black\'>' + package + '\s.*<td ' 
                            +'class=\'data[0-9]\'><span class=\'f4\'><span class=\'blue\''
                            + '>(.*?)</span>', html, re.DOTALL).groups()
                                  
        id = found[0]
        description = found[1]

        if id and description:
            msg = "" + package + " Descripccion: " + description + " 02http://aur.archlinux.org/packages.php?ID=" + str(id)  
        else:
            msg = "NO EXISTE EL PAQUETE, QUE QUIERES QUE TE LO CREE TAMBIEN"
                
        self.bot.sendtext(msg, True)
         
    
    #old pksearch code, here as backup
    def findInAur( self, package):
        
        html = urllib.urlopen('http://aur.archlinux.org/packages.php?setlang=en' +
                              '&do_Search=SeB=nd&L=0&C=0&PP=100&K=' + package).read()
                               
        found = (re.compile('packages.php\?ID=.*?><.*?>(.*?)</span>')).findall(html)

        return found
        
    
    def pkSearch(self, package):
        resp = []

        for repo in repos:
            resp = database.search().search(repo, package)
            if resp:
                break

        for pkg in self.findInAur(package):
            resp.append(pkg)
            
        if not resp:
            msg = "NO EXISTE EL PAQUETE, QUE QUIERES QUE TE LO CREE TAMBIEN"
        else:
            msg = (" || ").join(resp[:12])
            if len(resp) > 12:
                msg += " 01***SERE UN BOT PERO NO IDIOTA. SE MAS ESPECÍFIC@ QUE HAY MÁS DE 12 RESULTADOS***"
            
        self.bot.sendtext( msg, True)
        
    
    def __doc__( self ):
        self.bot.sendtext("USO: search [paquete], VAMOS NO ES TAN DIFICIL", True)
        self.bot.sendtext("acciones: search", True)
        
    def giveLinks( self, args):
        links = ["Archlinux: http://archlinux.org/", 
                 "Forums: http://bbs.archlinux.org/",
                 "Bugs: http://bugs.archlinux.org/",
                 "Wiki: http://wiki.archlinux.org/",
                 "Packages: http://aur.archlinux.org/packages.php",
                 "Get Arch: http://www.archlinux.org/download/"]
        
        msg = (" || ").join(links)
        
        self.bot.sendtext( msg, True)
        
    def handler(self, bot, cmd, args):
        self.bot = bot

        try:
            
            self.actions[cmd](args.strip())
                
        except:
            print "ERROR"
            self.__doc__()
