from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from .domain.match import Match
from .forms import MatchSettingsForm
from .services.main import create_match

MATCH_SESSION_KEY = "scoreboard_match"


def _save_match(request, match: Match) -> None:
    request.session[MATCH_SESSION_KEY] = match.to_session()


def _load_match(request) -> Match | None:
    data = request.session.get(MATCH_SESSION_KEY)
    if not data:
        return None
    try:
        return Match.from_session(data)
    except (KeyError, TypeError, ValueError):
        # Não deixe uma sessão antiga ou inválida inutilizar o placar.
        request.session.pop(MATCH_SESSION_KEY, None)
        return None


@require_GET
def home(request):
    return render(request, "home.html")


def setup(request):
    if request.method == "POST":
        form = MatchSettingsForm(request.POST)
        if form.is_valid():
            values = form.cleaned_data
            match = create_match(
                values["home_name"],
                values["away_name"],
                values["sets_to_win"],
                values["points_per_set"],
            )
            _save_match(request, match)
            return redirect("scoreboard")  # POST/Redirect/GET
    else:
        form = MatchSettingsForm()

    return render(request, "setup.html", {"form": form})


@require_GET
@ensure_csrf_cookie
def scoreboard(request):
    match = _load_match(request)
    if match is None:
        messages.info(request, "Crie uma partida antes de acessar o placar.")
        return redirect("setup")
    return render(request, "match.html", {"match": match})


def _match_json_response(match: Match, changed_team: str | None = None) -> JsonResponse:
    winner = match.match_winner()
    return JsonResponse({
        "status": "success",
        "score_a": match.home.points,
        "score_b": match.away.points,
        "sets_a": match.home.sets_won,
        "sets_b": match.away.sets_won,
        "current_set": match.current_set,
        "current_server": "A" if match.home.is_serving else "B",
        "set_finished": match.set_finished,
        "set_winner": match.set_winner_name.upper() if match.set_winner_name else None,
        "is_finished": match.match_is_over(),
        "match_winner": "A" if winner is match.home else "B" if winner is match.away else None,
        "can_undo": bool(match.point_history) and not match.set_finished,
        "can_undo_a": match.home.points > 0 and not match.set_finished and not match.match_is_over(),
        "can_undo_b": match.away.points > 0 and not match.set_finished and not match.match_is_over(),
        "changed_team": changed_team,
    })


def _action_error(message: str, *, code: str = "invalid_action", status: int = 409) -> JsonResponse:
    return JsonResponse({"status": "error", "code": code, "error": message}, status=status)


def _match_for_action(request):
    match = _load_match(request)
    if match is None:
        return None, _action_error(
            "Sua partida não está mais disponível. Crie outra.",
            code="match_unavailable",
        )
    return match, None


def _score_for_team(request, team_key: str):
    match, error = _match_for_action(request)
    if error:
        return error

    team = match.home if team_key == "home" else match.away
    if not match.score_point(team):
        return _action_error("Não foi possível registrar este ponto.")
    _save_match(request, match)
    return _match_json_response(match, "A" if team_key == "home" else "B")


@require_POST
def point_a(request):
    return _score_for_team(request, "home")


@require_POST
def point_b(request):
    return _score_for_team(request, "away")


@require_POST
def match_score(request):
    team_key = request.POST.get("team")
    if team_key not in ("home", "away"):
        return _action_error("Time inválido.", status=400)
    return _score_for_team(request, team_key)


@require_POST
def undo_score(request, team_key: str | None = None):
    match, error = _match_for_action(request)
    if error:
        return error

    if team_key is None:
        changed_team = match.point_history[-1] if match.point_history else None
        undone = match.undo_last_point()
    else:
        team = {"home": match.home, "away": match.away}.get(team_key)
        if team is None:
            return _action_error("Time inválido.", status=400)
        changed_team = team_key
        undone = match.undo_point(team)

    if not undone:
        return _action_error("Não há ponto para desfazer neste set.")
    _save_match(request, match)
    return _match_json_response(
        match,
        "A" if changed_team == "home" else "B" if changed_team == "away" else None,
    )


@require_POST
def reset_set(request):
    match, error = _match_for_action(request)
    if error:
        return error

    if not match.reset_current_set():
        return _action_error("Um set finalizado não pode ser reiniciado.")
    _save_match(request, match)
    return _match_json_response(match)


@require_POST
def next_set(request):
    match, error = _match_for_action(request)
    if error:
        return error

    if not match.advance_set():
        return _action_error("Finalize o set antes de iniciar o próximo.")
    _save_match(request, match)
    return _match_json_response(match)


@require_POST
def end_match(request):
    request.session.pop(MATCH_SESSION_KEY, None)
    return redirect("setup")
