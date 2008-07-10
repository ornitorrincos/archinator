import sys
import random, pickle
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
    	self.bot.sendtext('Uso: bofh', True)

    def handler(self, bot, cmd, args):
    	self.bot = bot
        
        random.shuffle( self.excuses )
        self.bot.sendtext(self.excuses[0].strip().replace("\n"," "), True)
        return True

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
