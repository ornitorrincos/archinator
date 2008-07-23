# -*- coding: utf-8 -*-

import re
import urllib
import feedparser
import database

repos = ('core', 'extra', 'community')

class main:
    
    def __init__( self, bot ):
        self.bot = ""
        self.actions = {'archnews'   : self.archnews,
                        'archlinks'  : self.giveLinks,
                        'pksearch'   : self.pkSearch,
                        'pkinfo'     : self.pkInfo,
                        'sqlinfo'    : self.sqlinfo,}
    
    def archnews( self, *args ):
        news = feedparser.parse("http://www.archlinux.org/feeds/news/")
        news = [ new['title'] for new in news['items'] if 'title' in new ]
        news = (" || ").join(news[:10])
        self.bot.sendtext(news, True)


    def pkSearch(self, package):
        self.resp = []
        for self.repo in repos:
            self.resp.append(database.search().sqlsearch(self.repo, package))
        
        self.resp += database.search().aurlsearch(package)
        self.msg = (' || ').join(self.resp[:12])
        
        self.bot.sendtext(str(self.msg), True)
    
    def sqlinfo(self, package):
        print 'sqlinfo'
        self.counter = 0
        print self.counter
        for self.repo in repos:
            try:
                self.resp = database.info().sqlinfo(self.repo, package)
            except PackageError(package):
                self.counter += 1
        if self.counter == 3:
            self.resp = 'Paquete no encontrado'
        self.bot.sendtext(str(self.resp), True)
    
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