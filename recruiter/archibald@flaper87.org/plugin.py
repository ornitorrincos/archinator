# -*- coding: utf-8 -*-

import re
import noapygoogle as nPyG

class main:
    
    def __init__( self, bot ):
        self.bot = ""
        self.actions = {'trans' : self.translate }
        
    def translate( self, word, lang ):
        
        deff = [result['definition'] for result in nPyG.translateWord( word, lang)['results']
                 if result['definition']]
                 
        deff = (' || ').join(deff)
        
        self.bot.sendtext(deff, True)
        
    def handler(self, bot, cmd, args):
        self.bot = bot
        
        try:
            if cmd == "trans":
                word, lang = (re.compile(r'(\w+)(.*)', re.DOTALL)).findall(args)[0]
                self.translate( word.strip(), lang.strip())
                
        except:
            self.__doc__()
