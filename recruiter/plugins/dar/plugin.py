# -*- coding: utf-8 -*-

import os

class main:
    
    def __init__( self, bot ):
        self.bot = ""
        self.actions = {'dar'   : self.handler}
        self.reqs = {'archlinks'  : self.giveLinks,
                     'errormsg'   : self.givErrormsg,
                     'cafe'       : self.giveCoffe}
    

    def giveCoffe( self, user ):
        msg = "da una manta y una taza de café a %s" % user
        self.bot.sendtext( 'PRIVMSG ' + self.bot.reqChannel + ' :\001ACTION %s\001' % msg )
        
    def givErrormsg( self, user ):
        self.bot.sendtext( 'PRIVMSG ' + self.bot.reqChannel + ' : ' + user + ' ➜ http://pics.ipostr.com/pics/pic_12047688966944.jpg \n' )
        
    def giveLinks( self, user):
        links = ["Archlinux: http://archlinux.org/", 
                 "Forums: http://bbs.archlinux.org/",
                 "Bugs: http://bugs.archlinux.org/",
                 "Wiki: http://wiki.archlinux.org/",
                 "Packages: http://aur.archlinux.org/packages.php",
                 "Get Arch: http://www.archlinux.org/download/"]
        
        msg = (" || ").join(links)

        self.bot.sendtext( 'PRIVMSG ' + self.bot.reqChannel + ' : ' + user + ' ➜ ' +  msg )
        
    def handler(self, bot, cmd, args):
        self.bot = bot
        
        args = args.split()
        
        self.reqs[args[1]](args[0])

