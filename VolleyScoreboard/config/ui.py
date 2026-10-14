import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_title():
    print(f"\n{'✩░▒▓▆▅▃▂▁𝐕𝐨𝐥𝐥𝐞𝐲𝐛𝐚𝐥𝐥 𝐒𝐜𝐨𝐫𝐞𝐛𝐨𝐚𝐫𝐝▁▂▃▅▆▓▒░✩':^60}")
    print('=' * 60)


def render_scoreboard(home, away, match):
    show_title()
    print(f"Set {match.current_set}/{match.total_sets}")
    print(f"{home.name:^28}{'':^4}{away.name:^28}")
    print(f"{'Pontos':<10}{home.points:^18}{away.points:^18}")
    print(f"{'Sets':<10}{home.sets_won:^18}{away.sets_won:^18}")
    server_name = home.name if home.is_serving else away.name
    print(f"\nSacando: {server_name}")
    print('=' * 60)


def show_message(text):
    print(f"\n{text}")


def wait_for_continue():
    input('\nPressione Enter para continuar...')
