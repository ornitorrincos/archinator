# -*- coding: utf-8 -*-

import os

class main:
    
    def __init__( self, bot ):
        self.bot = ""
        self.actions = {'dar'   : self.handler}
        self.reqs = {'errormsg'       : self.givErrormsg,
                     'cafe'           : self.giveCoffe,
                     'silencio'       : self.giveSilence,
                     'googleit'       : self.fuckinGoogleit,
                     'como-preguntar' : self.smartQuestions,
                     'consejo'        : self.giveConsejo,
                     'patada'         : self.givePatada,
                     'consuelo'       : self.giveConsuelo,
                     'galletitas'     : self.giveCookies,
                     'claro'          : self.giveClaro}
    

    def smartQuestions( self, user ):
        msg = "%s ➜ http://catb.org/esr/faqs/smart-questions.html" % user
        self.bot.sendtext( 'PRIVMSG ' + self.bot.reqChannel + ' :' + msg )
        
    def fuckinGoogleit( self, user ):
        msg = "%s ➜ http://www.justfuckinggoogleit.com/" % user
        self.bot.sendtext( 'PRIVMSG ' + self.bot.reqChannel + ' :' + msg )
    
    def giveSilence( self, user ):
        msg = "%s mando a decir %s que te CALLES!!" % (user, self.bot.reqUser )
        self.bot.sendtext( 'PRIVMSG ' + self.bot.reqChannel + ' :' + msg )
        
    def giveCoffe( self, user ):
        msg = "da una manta y una taza de café a %s" % user
        self.bot.sendtext( 'PRIVMSG ' + self.bot.reqChannel + ' :\001ACTION %s\001' % msg )

    def giveConsejo( self, user ):
        msg = user + " ahómbrese y no sea marica le dije"
        self.bot.sendtext( 'PRIVMSG ' + self.bot.reqChannel + ' :' + msg )

    def giveClaro( self, user ):
        msg = "me extraña dijo la araña mientras tejía su telaraña colgando de una guadaña hasta que llegó una musaraña toda malaentraña y la mató mi estimadísimo %s" % user
        self.bot.sendtext( 'PRIVMSG ' + self.bot.reqChannel + ' :\001ACTION %s\001' % msg )
        
    def givErrormsg( self, user ):
        self.bot.sendtext( 'PRIVMSG ' + self.bot.reqChannel + ' :' + user + ' ➜ http://ipo.totfarm.com/pics/pic_11995818968645.jpg' )
        
    def givePatada( self, user ):
        msg = "le da una patada en las bolas a %s" % user
        self.bot.sendtext( 'PRIVMSG ' + self.bot.reqChannel + ' :\001ACTION %s\001' % msg )
        
    def giveConsuelo( self, user ):
        msg = "le da palmaditas a  %s" % user
        self.bot.sendtext( 'PRIVMSG ' + self.bot.reqChannel + ' :\001ACTION %s\001' % msg )

    def giveCookies( self, user ):
        msg = "da unas galletitas de chocolate a %s con un vaso de leche" % user
        self.bot.sendtext( 'PRIVMSG ' + self.bot.reqChannel + ' :\001ACTION %s\001' % msg )

    def handler(self, bot, cmd, args):
        self.bot = bot
        
        args = args.split()
        
        if args[0] in self.bot.actions:
            self.bot.reqUser = args[1]
            self.bot.actions[args[0]].handler( self.bot, args[0], (' ').join(args[2:]))
        else:
            self.reqs[args[0]](args[1])

