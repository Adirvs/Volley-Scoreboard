from team import Team

class Match:

    def __init__(self, home: Team, away: Team, best_of: int, points_per_set: int):
        self.home = home
        self.away = away
        self.best_of = best_of
        self.points_per_set = points_per_set
        self.current_set = 1
        self.set_finished = False
        self.set_winner = False

    def score_point(self, team: Team):

        # Marca o ponto para a equipe e reseta o status de saque

        while not self.match_is_over():
            team.add_point()
            team.is_serving = True
            if team == self.home:
                self.away.is_serving = False
            else:
                self.home.is_serving = False

    def _point_difference(self) -> int:
        return abs(self.home.points - self.away.points)

    def check_set_winner(self):
        
        #Verifica se há um vencedor do set com base nos pontos e na diferença de pontos

        if self.home.points >= self.points_per_set and self.home.points > self.away.points and self._point_difference() >= 2:
            self.set_winner = True
            return self.home
        elif self.away.points >= self.points_per_set and self.away.points > self.home.points and self._point_difference() >= 2:
            self.set_winner = True
            return self.away
        return None

    def complete_set(self):
        winner = self.set_winner
        if winner:
            winner.win_set()
            self.set_finished = True
        return winner

    def reset_set(self):

        #reseta os pontos das equipes e define o status de saque para a equipe vencedora do set e reseta o status de set_finished e set_winner

        set_winner = self.check_set_winner()
        if set_winner:
            self.home.reset_points()
            self.away.reset_points()
            set_winner.is_serving = True
        self.set_finished = False
        self.set_winner = False

    def advance_set(self):
        while not self.match_is_over():
            if self.current_set < self.total_sets:
                self.reset_set()
                self.current_set += 1

    def match_winner(self):
        if self.home.sets_won >= self.best_of:
            return self.home
        if self.away.sets_won >= self.best_of:
            return self.away
        return None

    def match_is_over(self) -> bool:
        return self.match_winner() is not None