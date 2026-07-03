def _prompt_positive_int(prompt_text):
    while True:
        value = input(prompt_text)
        if value.isdigit() and int(value) > 0:
            return int(value)
        print('Entrada inválida. Digite um número inteiro positivo.')


def prompt_match_settings():
    home_name = input('Digite o nome do Time A: ').strip() or 'Time A'
    away_name = input('Digite o nome do Time B: ').strip() or 'Time B'
    total_sets = _prompt_positive_int('Digite a quantidade de sets: ')
    points_per_set = _prompt_positive_int('Digite a quantidade máxima de pontos por set: ')
    return home_name, away_name, total_sets, points_per_set


def prompt_score_action():
    while True:
        action = input('Digite 1 para Time A, 2 para Time B, r para reiniciar o set, x para sair: ').strip().lower()
        if action in ['1', '2', 'r', 'x']:
            return action
        print('Entrada inválida. Por favor, digite 1, 2, r ou x.')
