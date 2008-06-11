# -*- coding: utf-8 -*-

import re
import urllib
import feedparser

class main:
    
    def __init__( self, bot ):
        self.bot = bot
        self.actions = {'lastfm'   : self.getUserStats}
    
    def getUserStats( self, user ):

        news = feedparser.parse("http://ws.audioscrobbler.com/1.0/user/" + user + "/recenttracks.rss")
        
        if not news['items']:
            self.bot.sendtext('El usuario ' + user + ' no ' + 
                              'ha escuchado musica en una semana o màs. NO LE DARA VERGUENZA?, ' +
                              'Tambien puede ser que el usuario no exista. :-D', True)
            return True
        
        news = [ new['title'] for new in news['items'] if 'title' in new ]
        news = (" || ").join(news[:10])
        self.bot.sendtext(news.encode('utf-8'), True)
        
    def findComp( self, laster1, laster2):
        laster1 = urllib.urlopen("http://ws.audioscrobbler.com/1.0/user/" + laster1 + "/topartists.txt?type=overall").read()
        laster2 = urllib.urlopen("http://ws.audioscrobbler.com/1.0/user/" + laster2 + "/topartists.txt?type=overall").read()
        
        if not laster1 or not laster2:
            self.bot.sendtext("Uno de los usuarios no existe, verificar con el comando !lastfm", True)
            
        laster1 = dict((group, times) for times,group in (re.compile(r".*,(.*),(.*)\n")).findall(laster1))
        laster2 = dict((group, times) for times,group in (re.compile(r".*,(.*),(.*)\n")).findall(laster2))
        
        comp = [ group for group in laster1 if laster2.has_key(group)]
        if len(comp) <= 5:
            msg = "MALA: "
            pass
        elif len(comp) <=10:
            msg = "Media: "
            pass
        else:
            msg = "Alta: "

        msg += (",").join(comp)
        
        self.bot.sendtext(msg, True)
        
    def __doc__( self ):
        self.bot.sendtext("USO: search [paquete], VAMOS NO ES TAN DIFICIL", True)
        self.bot.sendtext("acciones: search", True)
        
    def handler(self, bot, cmd, args):

        internal = { "comp" : self.findComp} 
        try:
            param = (re.compile(r'(.*?)(?:\s|$)', re.DOTALL)).findall(args)[0]
            print param
            if param == "comp":
                user1, user2 = (re.compile(r'\w+\s(.*)\s(.*)')).findall(args)[0]
                print user1
                print user2
                self.findComp(user1, user2)
            else:
                self.getUserStats(param.strip())
                
        except:
            self.__doc__()
