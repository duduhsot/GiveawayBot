import random
from typing import List
from uuid import UUID
from userInfo import UserInfo

class Giveaway(object):
    
    def __init__(self,author :int,authorNick :str,name :str,description :str,NumberOfWinners :int,id :UUID,subscribers :List[UserInfo],ended :bool,winners :List[UserInfo],photoId :str):
        self.author = author
        self.authorNick = authorNick
        self.name = name
        self.description = description
        self.numberOfWinners = NumberOfWinners
        self.id = id
        self.subscribers = subscribers
        self.ended = ended
        self.winners = winners
        self.photoId = photoId

    def containsUser(self, user :UserInfo):
        return any(map(user.isSame, self.subscribers))

    def endGiveaway(self):
        # if subs.len < numOfWin => numOfWinners = subs.len
        self.numberOfWinners = min(self.numberOfWinners, len(self.subscribers))
        # generate winners
        subs = self.subscribers
        winners :List[UserInfo] = list()
        for i in range(0, self.numberOfWinners):
            newWinner = random.choice(subs)
            subs.remove(newWinner)
            winners.append(newWinner)
        # end giveaway
        self.ended = True
        self.winners = winners 

    def getWinners(self):
        if not self.ended:
            self.endGiveaway()
        # format winners in str
        winnersNames = [x.name for x in self.winners]
        winnersStr = '\n'.join(winnersNames)
        return winnersStr
