# -*- coding: utf-8 -*-

import re
import urllib

class main:
    
    def __init__( self, bot ):
        self.bot = ""
        self.actions = {'hora' : self.getTime }
        
    def getTime( self, code ):
        time = urllib.urlopen('http://www.worldtimeserver.com/current_time_in_' + code + '.aspx').read()
                               
        found = ((re.compile(r'<span class="font7">(.*?)</span>', re.DOTALL)).findall(time)[0]).strip()
        
        self.bot.sendtext(found, True)
        
    def __doc__( self ):
        self.bot.sendtext("USO: hora [codigo pais]", True)
        
    def handler(self, bot, cmd, args):
        self.bot = bot
        args = (args.strip()).upper()
        
        if len(args) > 2:
            self.__docs__()
        elif not args:
            args = "UTC"
            
        self.getTime(args)
