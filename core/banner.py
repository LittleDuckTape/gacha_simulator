import random
from core.rates import five_star_rate, four_star_rate

class Banner:
    def __init__(self, use_pity=True, use_5050=True):
        self.use_pity = use_pity
        self.use_5050 = use_5050
        
        self.pity = 0               # 5* count
        self.four_star_pity = 0     # 4* count
        self.guaranteed = False     # 50/50 flag

        self.total_pulls = 0

    def pull(self):
        self.total_pulls += 1
        self.pity += 1
        self.four_star_pity += 1

        # 5* check
        five_star_prob = (
            five_star_rate(self.pity) if self.use_pity else 0.006
        )

        if random.random() < five_star_prob:
            pity_hit = self.pity
            self.pity = 0
            self.four_star_pity = 0

            if not self.use_5050:
                return {"rarity": "5★", "type": "LIMITED", "pity": pity_hit}

            if self.guaranteed:
                self.guaranteed = False
                return {"rarity": "5★", "type": "LIMITED", "pity": pity_hit}

            if random.random() < 0.5:
                return {"rarity": "5★", "type": "LIMITED", "pity": pity_hit}
            else:
                self.guaranteed = True
                return {"rarity": "5★", "type": "STANDARD", "pity": pity_hit}
            
        # 4* check
        if random.random() < four_star_rate(self.four_star_pity):
            pity_hit = self.four_star_pity
            self.four_star_pity = 0
            return {"rarity": "4★", "pity": pity_hit}
        
        # 3* fallback
        return {"rarity": "3★"}