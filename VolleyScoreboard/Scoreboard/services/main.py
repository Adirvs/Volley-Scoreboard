"""Serviços de aplicação usados pelas views do placar."""

from ..domain.match import Match
from ..domain.team import Team


def create_match(home_name: str, away_name: str, sets_to_win: int, points_per_set: int) -> Match:
    home = Team(home_name)
    away = Team(away_name)
    home.is_serving = True
    return Match(home, away, sets_to_win, points_per_set)
