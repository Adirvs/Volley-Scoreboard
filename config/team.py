class Team:

    def __init__(self, name: str):
        self.name = name
        self.points = 0
        self.sets_won = 0
        self.is_serving = False

    def add_point(self):
        self.points += 1

    def reset_points(self):
        self.points = 0

    def win_set(self):
        self.sets_won += 1
