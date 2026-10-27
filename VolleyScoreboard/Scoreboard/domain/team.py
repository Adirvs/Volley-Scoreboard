class Team:
    def __init__(self, name: str):
        self.name = name
        self.points = 0
        self.sets_won = 0
        self.is_serving = False

    def add_point(self) -> None:
        self.points += 1

    def remove_point(self) -> bool:
        if self.points == 0:
            return False
        self.points -= 1
        return True

    def reset_points(self) -> None:
        self.points = 0

    def win_set(self) -> None:
        self.sets_won += 1
