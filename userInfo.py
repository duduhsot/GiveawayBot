from math import fabs
from telegram.update import Update

class UserInfo(object):
    
    def __init__(self, id :int, name :str):
        self.id :int = id
        self.name :str = name

    def isSame(self, oth :"UserInfo"):
        return self.id == oth.id

    def findSame(self, oths :list):
        for oth in oths:
            if self.isSame(oth):
                return oth
        return False