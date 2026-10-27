from django import forms


class MatchSettingsForm(forms.Form):
    home_name = forms.CharField(label="Nome do time A", max_length=100, initial="Time A")
    away_name = forms.CharField(label="Nome do time B", max_length=100, initial="Time B")
    sets_to_win = forms.IntegerField(
        label="Sets para vencer a partida", min_value=1, max_value=5, initial=3
    )
    points_per_set = forms.IntegerField(
        label="Pontos por set", min_value=1, max_value=50, initial=25
    )

    def clean(self):
        cleaned_data = super().clean()
        home = (cleaned_data.get("home_name") or "").strip()
        away = (cleaned_data.get("away_name") or "").strip()
        if home and away and home.casefold() == away.casefold():
            self.add_error("away_name", "Os times precisam ter nomes diferentes.")
        cleaned_data["home_name"] = home
        cleaned_data["away_name"] = away
        return cleaned_data
