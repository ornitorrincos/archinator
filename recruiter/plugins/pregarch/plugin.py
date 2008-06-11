import sys
import random, pickle
import re
from config import *

class main:

    def __init__( self, bot ):
        self.bot = ""
        self.quotes = ""
        self.quotesLoader()
        self.actions = ['pregarch']
            

    def quote(self, quote):
        for q in self.quotes: self.bot.sendtext(q, True)
        
    def quotesLoader( self):
        try:
            quotesFile = open( QUOTESFILE , 'r')
            self.quotes = (quotesFile.read()).split('\n')
            self.quotes.pop()
            quotesFile.close()
        except:
            pass

    def add(self, quote):
        try:
            if len(quote) < 3:
    			self.bot.sendtext('pregarch add <quote>', True)
    			return
   
            quotesFile = open( QUOTESFILE, 'a')
            quotesFile.write(quote + '\n')
            quotesFile.close()
            self.quotesLoader()
            self.bot.sendtext('Quote added', True)
    	except:
    		pass

    	
    def __doc__(self):
    	self.bot.sendtext('Uso: pregarch [add <quote>] [quotes]', True)

    def handler(self, bot, cmd, args):
    	self.bot = bot
        
    	if len(args) < 3:
    		random.shuffle( self.quotes )
    		self.bot.sendtext(self.quotes[0], True)
    		return True
    
    	comms = {
    		"add" : self.add,
    		"quotes" : self.quote,
    		"help" : self.__doc__
    	}
        	
    	try:
            reqaction, quote = (re.compile(r'(\w+)(.*)')).findall(args)[0]

            for action in comms.keys():
                if action == reqaction:
                    comms[action](quote)
                    break
    	except:
    	    self.__doc__()

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
