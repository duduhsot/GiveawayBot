
from giveaway import Giveaway
from database import giveaway_exists, load_giveaway, save_giveaway

newGiveaway :Giveaway= Giveaway(
    author = 1917,
    authorNick = "Mike",
    name = "test",
    description = "this is a test giveaway",
    NumberOfWinners = 5,
    id = UUID('726a4b5d-523b-467d-a75a-6090f0e66873'),
    subscribers = [],
    ended = False,
    winners = [],
    photoId = "some url"
)
save_giveaway(newGiveaway)
load_giveaway(str(newGiveaway.id))