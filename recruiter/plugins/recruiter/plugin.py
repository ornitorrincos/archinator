# -*- coding: utf-8 -*-

import re
import urllib

hispanicDomains = ['.ve', '.ar', '.mx', '.bo', '.cl', '.co', '.es', '.uy', '.pe', '.do', '.pr', '.py', '.pa']

class main:
    
    def __init__( self, bot ):
        self.bot = bot
        self.actions = {'addhost' : self.addhost }
        self.bot.listeners['JOIN'].append(self.listener) 
        self.nickslogged = []
        self.loadLogHosts()
        self.loadLogNicks()
        
    def addhost( self, host ):
        hostsLog = open('hostsLog', 'a')
        hostsLog.write(host + '\n')
        hostsLog.close()
        self.loadLogHosts()
        self.bot.sendtext(' The Host has been added', True)

    def loadLogHosts( self ):
        try:
            self.hostsLogged = hispanicDomains
            logHosts = open("hostsLog", "r")
            self.hostsLogged += (logHosts.read()).split('\n')
            logHosts.close()
            print self.hostsLogged
        except:
            pass                
        
    def loadLogNicks( self ):
        try:
            logNicks = open("nicksLog", "r")
            self.nickslogged = (logNicks.read()).split('\n')
            logNicks.close()
        except:
            pass
    
    def logNick( self, nick ):
        if not nick.lower() in self.nickslogged:
            logNicks = open("nicksLog", "a")
            logNicks.write(nick.lower() + '\n')
            logNicks.close()
            self.loadLogNicks()
            
    def listener( self, msg ):
        complete = msg[1:].split(':',1) #Parse the message into useful data
        
        try:
            joinerHost = (re.compile(r'@(.*)\sJOIN')).findall(msg)[0]
            #if re.match(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', joinerHost):
             #   joinerHost = (os.popen("host " + joinerHost).readlines())[0]
            joinerNick = ((re.compile(r':(.*)!')).findall(msg))[0]
        except:
            return

        if joinerHost and joinerNick:
            if joinerNick != self.bot.botnick and len([ x for x in self.hostsLogged if x in joinerHost ]) > 0 and not joinerNick.lower() in self.nickslogged:
                self.logNick( joinerNick )
                self.bot.sendtext('PRIVMSG flaper87 :Checkout, ' + joinerNick + ', ' + joinerHost)
                     
    def handler(self, bot, cmd, args):
        args = args.strip()
        print self.bot.botowners
        print self.bot.reqUser.lower()
        print self.hostsLogged
        if cmd == "addhost" and self.bot.reqUser.lower() in self.bot.botowners and not args in self.hostsLogged:
            self.addhost(args)
        elif self.bot.reqUser.lower() not in self.bot.botowners:
            self.bot.sendtext('PRIVMSG ' + channel + ' :' + user + ' You are not the bot owner.')
        elif args in self.hostsLogged:
            self.bot.sendtext('PRIVMSG ' + channel + ' :' + user + ' The Host already exists')
