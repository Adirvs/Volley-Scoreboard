#PROVAVELMENTE NÃO USADO POR CONTA DO is_valid()

def _prompt_positive_int(prompt_text):
    while True:
        value = input(prompt_text)
        if value.isdigit() and int(value) > 0:
            return int(value)
        print('Entrada inválida. Digite um número inteiro positivo.')

#--------------------------------------------------

from django import forms

class MatchSettingsForm(forms.Form):
    home_name = forms.CharField(label='Nome do Time A', max_length=100, initial='Time A')
    away_name = forms.CharField(label='Nome do Time B', max_length=100, initial='Time B')
    total_sets = forms.IntegerField(label='Quantidade de Sets', min_value=1, initial=3)
    points_per_set = forms.IntegerField(label='Pontos por Set', min_value=1, initial=25)

#PROVAVELMENTE TAMBÉM NÃO USADO POR CONTA DE BOTÕES NA INTERFACE GRÁFICA, MAS PODE SER ÚTIL PARA TESTES EM LINHA DE COMANDO

def prompt_score_action():
    while True:
        action = input('Digite 1 para Time A, 2 para Time B, r para reiniciar o set, x para sair: ').strip().lower()
        if action in ['1', '2', 'r', 'x']:
            return action
        print('Entrada inválida. Por favor, digite 1, 2, r ou x.')

#------------------------------------------------------