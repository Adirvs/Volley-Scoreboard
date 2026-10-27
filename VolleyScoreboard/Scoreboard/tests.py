from django.test import Client, TestCase
from django.urls import reverse

from .domain.match import Match
from .domain.team import Team


class MatchDomainTests(TestCase):
    def test_points_sets_undo_and_session_round_trip(self):
        home, away = Team("Azul"), Team("Verde")
        home.is_serving = True
        match = Match(home, away, sets_to_win=2, points_per_set=1)

        self.assertTrue(match.score_point(home))
        self.assertTrue(match.score_point(home))
        self.assertTrue(match.set_finished)
        self.assertEqual(home.sets_won, 1)
        self.assertFalse(match.undo_last_point())

        self.assertTrue(match.advance_set())
        self.assertEqual(match.current_set, 2)
        self.assertEqual((home.points, away.points), (0, 0))
        self.assertTrue(match.score_point(away))
        self.assertTrue(match.undo_last_point())
        self.assertEqual(away.points, 0)

        restored = Match.from_session(match.to_session())
        self.assertEqual(restored.current_set, 2)
        self.assertEqual(restored.home.name, "Azul")
        self.assertEqual(restored.away.points, 0)


class MatchViewsTests(TestCase):
    def create_match(self, **overrides):
        data = {
            "home_name": "Azul",
            "away_name": "Verde",
            "sets_to_win": 2,
            "points_per_set": 1,
        }
        data.update(overrides)
        return self.client.post(reverse("setup"), data)

    def test_setup_creates_serializable_match_and_redirects(self):
        response = self.create_match()
        self.assertRedirects(response, reverse("scoreboard"))

        session_match = self.client.session["scoreboard_match"]
        self.assertEqual(session_match["home"]["name"], "Azul")
        self.assertEqual(session_match["sets_to_win"], 2)
        self.assertContains(self.client.get(reverse("scoreboard")), "Azul")

    def test_scoring_finishes_set_then_next_set_resets_points(self):
        self.create_match()
        for _ in range(2):
            response = self.client.post(reverse("match_score"), {"team": "home"})
            self.assertRedirects(response, reverse("scoreboard"))

        response = self.client.get(reverse("scoreboard"))
        self.assertContains(response, "Azul venceu o set")
        self.assertEqual(self.client.session["scoreboard_match"]["home"]["sets_won"], 1)

        self.client.post(reverse("next_set"))
        session_match = self.client.session["scoreboard_match"]
        self.assertEqual(session_match["current_set"], 2)
        self.assertEqual(session_match["home"]["points"], 0)

    def test_mutating_url_rejects_get_and_template_includes_csrf(self):
        self.assertEqual(self.client.get(reverse("match_score")).status_code, 405)
        response = self.client.get(reverse("setup"))
        self.assertContains(response, "csrfmiddlewaretoken")

        csrf_client = Client(enforce_csrf_checks=True)
        self.assertEqual(
            csrf_client.post(reverse("setup"), {
                "home_name": "Azul", "away_name": "Verde",
                "sets_to_win": 2, "points_per_set": 25,
            }).status_code,
            403,
        )
