import random
from core.rates import five_star_rate

class Banner:
    def __init__(self, use_pity=True, use_50_50=True):
        self.pity = 0
        self.guaranteed = False #lost last 50/50 so next is guaranteed to be limited
        self.use_pity = use_pity
        self.use_50_50 = use_50_50

    def pull(self):
        self.pity += 1

        #picking probability model
        if self.use_pity:
            prob = five_star_rate(self.pity)
        else:
            prob = 0.006 #base rate (no pity)

        if random.random() < prob:
            #hit a 5*
            self.pity = 0

            if self.guaranteed:
                self.guaranteed = False
                return "LIMITED"

            if not self.use_50_50:
                return "LIMITED"
            
            #50/50
            if random.random() < 0.5:
                return "LIMITED"
            else:
                self.guaranteed = True
                return "STANDARD"
            
        return "NO 5★"