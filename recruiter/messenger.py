import threading
import re

class threader(threading.Thread):
    
    def __init__( self, bot, msg ):
        threading.Thread.__init__(self)
        self.bot = bot
        self.msg = msg
        
    def run( self ):
        try:
            if re.match(r':.*!.*PRIVMSG\s.*\s:!(.*)', self.msg, re.DOTALL):
                realMessage = (re.compile(r':(.*)!.*PRIVMSG\s(.*)\s:!(.*)')).findall(self.msg)[0]
            else:
                realMessage = (re.compile(r':(.*)!.*PRIVMSG\s(.*)\s:' + NICK + '\s(.*)')).findall(self.msg)[0]

            self.bot.reqUser = realMessage[0]
            self.bot.reqChannel = realMessage[1]
            action, self.msg = (re.compile(r'(\w+)(.*)')).findall(realMessage[2])[0]

            if self.bot.reqChannel == self.bot.botnick:
                self.bot.privReply = True
            else:
                self.bot.privReply = False

            if action in self.bot.defaultactions.keys():
                self.bot.defaultactions[action](self.msg)
                pass    
            elif action in self.bot.actions.keys():
                self.bot.actions[action].handler( self.bot, action, self.msg.strip())        
        except:
            print "ERROR"
            return