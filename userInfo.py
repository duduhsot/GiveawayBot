from math import fabs
from telegram.update import Update

class UserInfo(object):
    
    def __init__(self,update :Update):
        self.id = update.effective_user.id, 
        self.name = update.effective_user.name

    def isSame(self, oth :"UserInfo"):
        return self.id == oth.id

    def findSame(self, oths :list):
        for oth in oths:
            if self.isSame(oth):
                return oth
        return False