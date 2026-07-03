from match import Match
from team import Team
from prompts import prompt_match_settings, prompt_score_action
from ui import clear_screen, render_scoreboard, show_message, wait_for_continue, show_title


def setup_match():
    home_name, away_name, total_sets, points_per_set = prompt_match_settings()
    home = Team(home_name)
    away = Team(away_name)
    home.is_serving = True
    match = Match(home, away, total_sets, points_per_set)
    return home, away, match


def main():
    show_title()
    home, away, match = setup_match()

    while True:
        clear_screen()
        render_scoreboard(home, away, match)
        action = prompt_score_action()

        if action == 'x':
            break
        if action == 'r':
            match.reset_set()
            show_message('Set reiniciado.')
            wait_for_continue()
            continue

        scorer = home if action == '1' else away
        match.score_point(scorer)
        set_winner = match.complete_set()

        if set_winner:
            show_message(f'Vitória! O time {set_winner.name} venceu o set.')
            match_winner = match.match_winner()

            if match_winner:
                clear_screen()
                render_scoreboard(home, away, match)
                show_message(f'Vitória! O time {match_winner.name} venceu a partida!')
                break

            show_message('O placar será resetado para o próximo set.')
            wait_for_continue()
            match.advance_set()
            match.reset_set()

    show_message('Obrigado por usar o placar de voleibol.')
    restart = input('Deseja jogar novamente? (s/n): ').strip().lower()
    if restart == 's':
        main()
    else:
        show_message('Até a próxima!')

if __name__ == '__main__':
    main()
