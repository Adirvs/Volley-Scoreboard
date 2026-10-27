from .team import Team


class Match:
    """Regras de uma partida, sem depender de Django ou de persistência."""

    def __init__(self, home: Team, away: Team, sets_to_win: int, points_per_set: int):
        if home.name == away.name:
            raise ValueError("Os times precisam ter nomes diferentes.")
        if sets_to_win < 1 or points_per_set < 1:
            raise ValueError("A configuração da partida é inválida.")

        self.home = home
        self.away = away
        self.sets_to_win = sets_to_win
        self.points_per_set = points_per_set
        self.current_set = 1
        self.set_finished = False
        self.set_winner_name = None
        self.point_history = []

    def score_point(self, team: Team) -> bool:
        """Registra um ponto e encerra o set automaticamente quando necessário."""
        if self.match_is_over() or self.set_finished or team not in (self.home, self.away):
            return False

        team.add_point()
        self.point_history.append("home" if team is self.home else "away")
        self._set_server(team)

        winner = self.check_set_winner()
        if winner:
            self.complete_set(winner)
        return True

    def undo_last_point(self) -> bool:
        if self.set_finished or not self.point_history:
            return False

        side = self.point_history.pop()
        team = self.home if side == "home" else self.away
        team.remove_point()
        self._set_server(self.home if not self.point_history else
                         (self.home if self.point_history[-1] == "home" else self.away))
        return True

    def _set_server(self, team: Team) -> None:
        self.home.is_serving = team is self.home
        self.away.is_serving = team is self.away

    def _point_difference(self) -> int:
        return abs(self.home.points - self.away.points)

    def check_set_winner(self):
        for team, other in ((self.home, self.away), (self.away, self.home)):
            if team.points >= self.points_per_set and team.points > other.points and self._point_difference() >= 2:
                return team
        return None

    def complete_set(self, winner: Team = None):
        if self.set_finished:
            return self.set_winner()

        winner = winner or self.check_set_winner()
        if winner is None:
            return None

        winner.win_set()
        self.set_finished = True
        self.set_winner_name = "home" if winner is self.home else "away"
        return winner

    def set_winner(self):
        if self.set_winner_name == "home":
            return self.home
        if self.set_winner_name == "away":
            return self.away
        return None

    def reset_current_set(self) -> bool:
        """Limpa somente o set em andamento; sets já vencidos não são alterados."""
        if self.set_finished or self.match_is_over():
            return False
        self.home.reset_points()
        self.away.reset_points()
        self.point_history = []
        self._set_server(self.home)
        return True

    def advance_set(self) -> bool:
        if not self.set_finished or self.match_is_over():
            return False

        winner = self.set_winner()
        self.current_set += 1
        self.home.reset_points()
        self.away.reset_points()
        self.point_history = []
        self.set_finished = False
        self.set_winner_name = None
        self._set_server(winner or self.home)
        return True

    def match_winner(self):
        if self.home.sets_won >= self.sets_to_win:
            return self.home
        if self.away.sets_won >= self.sets_to_win:
            return self.away
        return None

    def match_is_over(self) -> bool:
        return self.match_winner() is not None

    def to_session(self) -> dict:
        """Converte o estado em tipos que a sessão padrão do Django serializa."""
        return {
            "home": {"name": self.home.name, "points": self.home.points, "sets_won": self.home.sets_won,
                     "is_serving": self.home.is_serving},
            "away": {"name": self.away.name, "points": self.away.points, "sets_won": self.away.sets_won,
                     "is_serving": self.away.is_serving},
            "sets_to_win": self.sets_to_win,
            "points_per_set": self.points_per_set,
            "current_set": self.current_set,
            "set_finished": self.set_finished,
            "set_winner_name": self.set_winner_name,
            "point_history": list(self.point_history),
        }

    @classmethod
    def from_session(cls, data: dict):
        def build_team(team_data):
            team = Team(team_data["name"])
            team.points = team_data["points"]
            team.sets_won = team_data["sets_won"]
            team.is_serving = team_data["is_serving"]
            return team

        home = build_team(data["home"])
        away = build_team(data["away"])
        match = cls(home, away, data["sets_to_win"], data["points_per_set"])
        match.current_set = data["current_set"]
        match.set_finished = data["set_finished"]
        match.set_winner_name = data["set_winner_name"]
        match.point_history = list(data["point_history"])
        return match
