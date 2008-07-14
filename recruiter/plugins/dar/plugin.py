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
                     'consejo'        : self.giveConsejo}
    

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
        msg = "da una manta y una taza de café colombiano a %s" % user
        self.bot.sendtext( 'PRIVMSG ' + self.bot.reqChannel + ' :\001ACTION %s\001' % msg )

    def giveConsejo( self, user ):
        msg = user + " ahómbrese y no sea marica le dije"
        self.bot.sendtext( 'PRIVMSG ' + self.bot.reqChannel + ' :' + msg )
        
    def givErrormsg( self, user ):
        self.bot.sendtext( 'PRIVMSG ' + self.bot.reqChannel + ' :' + user + ' ➜ http://pics.ipostr.com/pics/pic_12047688966944.jpg \n' )
        
    def handler(self, bot, cmd, args):
        self.bot = bot
        
        args = args.split()
        
        if args[1] in self.bot.actions:
            self.bot.reqUser = args[0]
            self.bot.actions[args[1]].handler( self.bot, args[1], (' ').join(args[2:]))
        else:
            self.reqs[args[1]](args[0])

