from team import Team

class Match:

    def __init__(self, home: Team, away: Team, total_sets: int, points_per_set: int):
        self.home = home
        self.away = away
        self.total_sets = total_sets
        self.points_per_set = points_per_set
        self.current_set = 1

    def score_point(self, team: Team):
        team.add_point()
        team.is_serving = True
        if team == self.home:
            self.away.is_serving = False
        else:
            self.home.is_serving = False

    def _point_difference(self) -> int:
        return abs(self.home.points - self.away.points)

    def set_winner(self):
        if self.home.points >= self.points_per_set and self.home.points > self.away.points and self._point_difference() >= 2:
            return self.home
        elif self.away.points >= self.points_per_set and self.away.points > self.home.points and self._point_difference() >= 2:
            return self.away
        else:
            return None

    def complete_set(self):
        winner = self.set_winner()
        if winner:
            winner.win_set()
        return winner

    def reset_set(self):
        self.home.reset_points()
        self.away.reset_points()

    def advance_set(self):
        if self.current_set < self.total_sets:
            self.current_set += 1

    def needed_sets_to_win(self) -> int:
        return self.total_sets // 2 + 1

    def match_winner(self):
        if self.home.sets_won >= self.needed_sets_to_win():
            return self.home
        if self.away.sets_won >= self.needed_sets_to_win():
            return self.away
        return None

    def is_match_over(self) -> bool:
        return self.match_winner() is not None