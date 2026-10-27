from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("match/new/", views.setup, name="setup"),
    path("match/", views.scoreboard, name="scoreboard"),
    path("match/score/", views.match_score, name="match_score"),
    path("match/undo/", views.undo_score, name="undo_score"),
    path("match/reset/", views.reset_set, name="reset_set"),
    path("match/next-set/", views.next_set, name="next_set"),
    path("match/end/", views.end_match, name="end_match"),
]
