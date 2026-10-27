from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST

from .domain.match import Match
from .forms import MatchSettingsForm
from .services.main import create_match

MATCH_SESSION_KEY = "scoreboard_match"


def _save_match(request, match):
    request.session[MATCH_SESSION_KEY] = match.to_session()


def _load_match(request):
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
def scoreboard(request):
    match = _load_match(request)
    if match is None:
        messages.info(request, "Crie uma partida antes de acessar o placar.")
        return redirect("setup")
    return render(request, "match.html", {"match": match})


def _match_for_action(request):
    match = _load_match(request)
    if match is None:
        messages.info(request, "Sua partida não está mais disponível. Crie outra.")
        return None
    return match


@require_POST
def match_score(request):
    match = _match_for_action(request)
    if match is None:
        return redirect("setup")

    team = {"home": match.home, "away": match.away}.get(request.POST.get("team"))
    if team is None or not match.score_point(team):
        messages.error(request, "Não foi possível registrar este ponto.")
    _save_match(request, match)
    return redirect("scoreboard")


@require_POST
def undo_score(request):
    match = _match_for_action(request)
    if match is None:
        return redirect("setup")

    if not match.undo_last_point():
        messages.info(request, "Não há ponto para desfazer neste set.")
    _save_match(request, match)
    return redirect("scoreboard")


@require_POST
def reset_set(request):
    match = _match_for_action(request)
    if match is None:
        return redirect("setup")

    if not match.reset_current_set():
        messages.info(request, "Um set já finalizado não pode ser reiniciado.")
    _save_match(request, match)
    return redirect("scoreboard")


@require_POST
def next_set(request):
    match = _match_for_action(request)
    if match is None:
        return redirect("setup")

    if not match.advance_set():
        messages.info(request, "Finalize o set antes de iniciar o próximo.")
    _save_match(request, match)
    return redirect("scoreboard")


@require_POST
def end_match(request):
    request.session.pop(MATCH_SESSION_KEY, None)
    return redirect("setup")
