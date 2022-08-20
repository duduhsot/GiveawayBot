
class MessageChecker(object):
    
    def __init__(self,keyWords,score,currency,message):
        self.keyWords = keyWords
        self.score = score
        self.message = message
        self.currency = currency

    def check(self,text:str):
        return any(map(text.__contains__, self.keyWords))

    def reply(self):
        return '%s %s %s!' % (self.message, str(self.score), self.currency) 