class Time:

    def __init__(self, nome):
        self.nome = nome
        self.score = 0

    def score_point(self):
        self.score += 1
    
    def reset(self):
        self.score = 0