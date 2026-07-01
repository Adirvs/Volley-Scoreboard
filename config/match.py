from team import Time

class Match:

    def __init__(self, time1, time2, set_amount, maxpoints):
        self.time1 = time1
        self.time2 = time2
        self.set = set_amount
        self.maxpoints = maxpoints
    
    def score_point(self, time):
        time.score_point()
        time.is_serving = True
        if time == self.time1:
            self.time2.is_serving = False
        else:
            self.time1.is_serving = False

    def check_setwin(self):
        diff = abs(self.time1.score - self.time2.score)
        if self.time1.score >= self.time2.score and self.time1.score >= self.maxpoints and diff >=2:
            self.time1.set_won()
            return f"Vitória! O time {self.time1.nome} venceu o set!"
        elif self.time2.score >= self.time1.score and self.time2.score >= self.maxpoints and diff >=2:
            self.time2.set_won()
            return f"Vitória! O time {self.time2.nome} venceu o set!"
        else:
            return f"Ainda não há um vencedor"
    
    def reset(self):
        self.time1.reset()
        self.time2.reset()
    
    def check_matchwin(self):
        if self.time1.set > (self.set/2):
            return f"Vitória! O time {self.time1.nome} venceu a partida!"
        elif self.time2.set > (self.set/2):
            return f"Vitória! O time {self.time2.nome} venceu a partida!"
        else:
            return f"Ainda não há um vencedor da partida"