from team import Time

class Match:

    def __init__(self, time1, time2, maxpoints):
        self.time1 = time1
        self.time2 = time2
        self.maxpoints = maxpoints
    
    def score_point(self, time):
        time.score_point()
        print(f"O time {time.nome} marcou 1 ponto!")
    
    def check_win(self):
        diff = abs(self.time1.score - self.time2.score)
        while True:
            if self.time1.score >= self.maxpoints and diff >=2:
                return f"Vitória! O time {self.time1} venceu a partida!"
                break
            elif self.time2.score >= self.maxpoints and diff >=2:
                return f"Vitória! O time {self.time2} venceu a partida!"
                break
            else:
                return f"Ainda não há um vencedor"
    
    def reset(self):
        self.time1.reset()
        self.time2.reset()

time1 = Time("Catherine")
time2 = Time("Joseph")

partida = Match(time1, time2, 15)

Match.check_win(partida)

