import sys
from random import choice
import re
from config import *

class main:

    def __init__( self, bot ):
        self.bot = ""
        self.excuses = ""
        self.bofhLoader()
        self.actions = ['bofh']
        
    def bofhLoader( self):
        try:
            bofhFile = open( BOFHSFILE, 'r')
            self.excuses = (bofhFile.read()).split('%')
            self.excuses.pop()
            bofhFile.close()
        except:
            pass

    	
    def __doc__(self):
    	self.bot.sendtext('Uso: bofh [ numero ]', True)

    def handler(self, bot, cmd, args):
        try:
            self.bot = bot
            
            if args:
                self.bot.sendtext(self.excuses[args.strip()].strip().replace("\n"," "), True)
            else:
                self.bot.sendtext(choice(self.excuses).strip().replace("\n"," "), True)
            return True
        except:
            self.__doc__()

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
