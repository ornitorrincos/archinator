# -*- coding: utf-8 -*-

import re
import urllib

class main:
    
    def __init__( self, bot ):
        self.bot = ""
        self.actions = {'chiste' : self.search }
        
    def search( self ):
        html = urllib.urlopen('http://www.chistes.com/ChisteAlAzar.asp').read()
                               
        found = ((((re.compile('<div class="chiste">(.*?)</div>', re.DOTALL)).findall(html)[0]).replace("<BR>", " ")).replace("\n", "")).replace("\r", "")
        
        if len(found) >= 400:
            found = found.split(" ")
            pack1 = (" ").join(found[:60])
            pack2 = (" ").join(found[60:])
            self.bot.sendtext(pack1, True)
            self.bot.sendtext(pack2, True)
        else:
            self.bot.sendtext(found, True)
        
    def handler(self, bot, cmd, args):
        self.bot = bot
        self.search()
