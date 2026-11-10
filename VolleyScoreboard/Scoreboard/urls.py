from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("match/new/", views.setup, name="setup"),
    path("match/", views.scoreboard, name="scoreboard"),
    path("match/point/a/", views.point_a, name="point_a"),
    path("match/point/b/", views.point_b, name="point_b"),
    path("match/undo/a/", views.undo_score, {"team_key": "home"}, name="undo_a"),
    path("match/undo/b/", views.undo_score, {"team_key": "away"}, name="undo_b"),
    path("match/next-set/", views.next_set, name="next_set"),
    path("match/reset/", views.reset_set, name="reset_set"),
    # Mantém os endpoints existentes para clientes que ainda os utilizem.
    path("match/score/", views.match_score, name="match_score"),
    path("match/undo/", views.undo_score, name="undo_score"),
    path("match/end/", views.end_match, name="end_match"),
]
