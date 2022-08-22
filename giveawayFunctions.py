import os
import pickle
from pyclbr import Function

from giveaway import Giveaway

def loadGiveaway(giveawayId:str):
    with open(os.path.join(GIVEAWAYS_PATH, 'g_%s.pkl' % giveawayId), 'rb') as giveaway_file:
        giveaway :Giveaway = pickle.load(giveaway_file)
        return giveaway

def saveGiveaway(giveaway :Giveaway):
    if not os.path.exists(GIVEAWAYS_PATH):
        os.mkdir(GIVEAWAYS_PATH)
    with open(os.path.join(GIVEAWAYS_PATH, 'g_%s.pkl' % giveaway.id), 'wb') as giveaway_file:
        pickle.dump(giveaway, giveaway_file)
