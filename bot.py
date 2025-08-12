import random

class Bot:
    def __init__(self, name, chips, cards=None, bot=True):
        self.name = name
        self.chips = 500
        self.cards = cards
        self.put_in = 0
        self.bot = bot
        self.fold = False
    
    def logic(self, put_in, bet, hand, pot, round):
        if bet-put_in == 0:
            return "Check"
        if random.randint(0,1) != 0:
            self.chips -= (bet-put_in)
            return "Call: " + str(int(bet-put_in))
        elif random.randint(0, 100) == 0:
            self.chips -= (bet-put_in) * 2
            return "Raise: " + str(int((bet-put_in) * 2))
        else:
            self.fold = True
            return "Fold"
