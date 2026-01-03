import random
from core.rates import five_star_rate

class Banner:
    def __init__(self):
        self.pity = 0
        self.guaranteed = False #lost last 50/50 so next is guaranteed to be limited

    def pull(self):
        self.pity += 1

        if random.random() < five_star_rate(self.pity):
            #hit a 5*
            self.pity = 0

            if self.guaranteed:
                self.guaranteed = False
                return "LIMITED"
            
            #50/50
            if random.random() < 0.5:
                return "LIMITED"
            else:
                self.guaranteed = True
                return "STANDARD"
            
        return "NO 5★"