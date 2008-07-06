# -*- coding: utf-8 -*-

import re
import socket
import os
import sys
import messenger
import time
from config import *

class rEcRuItEr:
	
	def __init__( self ): 
		self.socket = ""
		self.botowners = OWNERS
		self.botnick  = NICK
		self.privReply = False
		self.listeners = { 'JOIN' : []}
		self.defaultactions   = { "commands" : self.showCommands,
								  "restart"  : self.restart,
								  "muere"      : self.quit}
		self.actions  = {}
		self.plugins   = {}
		self.loadPlugins()
		self.connect()
	
	def loadPlugins( self ):
		for plugin in ENABLEDPLUGINS:
			current = __import__('plugins.' + plugin + '.plugin', globals(), locals(), [''])
			self.plugins[plugin] = current.main( self )

			for action in self.plugins[plugin].actions:
				if action in self.actions:
					print "Action " + action + "From " + plugin + "is duplicated"
					continue
				self.actions[action] = self.plugins[plugin]
				
			print self.listeners
		
	def connect( self ):
		self.work = True
		self.socket = socket.socket( )
		self.socket.connect((HOST, PORT)) #Open the socket and Connect to server
		self.sendtext('NICK ' + NICK + '\n') #Send the nick to server
		self.sendtext('USER ' + IDENT + ' ' + HOST + ' bla :' + REALNAME + '\n') #Identify to server
		self.sendtext('PRIVMSG NICKSERV :IDENTIFY '+PASSWORD+'\n')
		self.sendtext('JOIN ' + CHANNELINIT + '\n')
		
		while self.work:
		    msg = self.socket.recv(500) #recieve server messages
		    if msg == "":
		    	continue
		    print '> '+msg.strip()
			
		    if msg.find('JOIN') != -1 and self.listeners['JOIN']: 
		    	for listener in self.listeners['JOIN']:
		    		listener( msg )
		    if re.match(r'.*(PRIVMSG)\s(.*)\s:' + NICK, msg) != -1: 
		    	messenger.threader( self, msg).start()
		    	
	def restart( self, args ):
		self.sendtext("QUIT reiniciandome NO ME EXTRAÑEN :P")
		self.work = False
		self.socket.close()
		self.connect()
		
	def quit( self, args ):
		if self.reqUser.lower() in self.botowners:
			os._exit(0)
		else:
			self.sendtext("Y por que yo? AHHH?... Acaso eres mi dueño??? Ve a matar a otro... :@", True)
	
	def sendtext( self, text, reply=False ):

		if reply and self.privReply:
			self.socket.send('PRIVMSG ' + self.reqUser + ' :' +  text +'\n')
		elif reply and not self.privReply:
			self.socket.send('PRIVMSG ' + self.reqChannel + ' :' + self.reqUser + ' ➜ ' +  text +'\n')
		else:
			self.socket.send(text +'\n')
			
	def showCommands( self, args ):
		self.sendtext((',').join(self.actions.keys()), True)
		
	def showPlugins( self, args ):
		self.sendtext((',').join(self.plugins.keys()), True)


rEcRuItEr()

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
