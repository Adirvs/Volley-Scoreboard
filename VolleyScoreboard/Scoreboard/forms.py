from django import forms

class MatchSettingsForm(forms.Form):

    home_name = forms.CharField(
        label='Nome do Time A',
        max_length=100,
        initial='Time A'
        )
    
    away_name = forms.CharField(
        label='Nome do Time B',
        max_length=100,
        initial='Time B'
        )
    
    total_sets = forms.IntegerField(
        label='Sets para vencer a partida',
        min_value=1,
        max_value=5,
        initial=3
        )
    
    points_per_set = forms.IntegerField(
        label='Pontos por Set',
        min_value=1,
        max_value=50,
        initial=25
        )
