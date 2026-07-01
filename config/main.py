from match import Match
from team import Time
import os


def system_clear():
    os.system('cls')

def title():
    print(f"\n{'✩░▒▓▆▅▃▂▁𝐕𝐨𝐥𝐥𝐞𝐲𝐛𝐚𝐥𝐥 𝐒𝐜𝐨𝐫𝐞𝐛𝐨𝐚𝐫𝐝▁▂▃▅▆▓▒░✩':^40}")
    print(f"{'='*40}\n")

def show_scoreboard(time1, time2):
    title()
    print(f"Placar: {time1.nome} {time1.score} x {time2.score} {time2.nome}")
    print(f"Sets: {time1.nome} {time1.set} x {time2.set} {time2.nome}")
    print(f"Sacando: {time1.nome if time1.is_serving else time2.nome}")
    print(f"\n{'='*40}\n")


def setup():
    title()
    time1 = Time(input("Digite o nome do Time A: "))
    time2 = Time(input("Digite o nome do Time B: "))
    match = Match(time1, time2, int(input("Digite a quantidade de sets: ")), int(input("Digite a quantidade máxima de pontos por set: ")))
    return time1, time2, match


def get_user_input():
    while True:
        user_input = input("Digite o número do time que marcou o ponto (1 ou 2), ou 'x' para sair: ")
        if user_input in ['1', '2', 'x']:
            return user_input
        else:
            print("Entrada inválida. Por favor, digite 1, 2 ou x.")
            

def main():
    time1, time2, match = setup()
    while True:
        system_clear()
        show_scoreboard(time1, time2)
        user_input = get_user_input()

        if user_input == 'x':
            break
        elif user_input == '1':
            match.score_point(time1)
        elif user_input == '2':
            match.score_point(time2)

        result = match.check_setwin()

        if "Vitória" in result:
            if "Vitória" in match.check_matchwin():
                system_clear()
                show_scoreboard(time1, time2)
                print(match.check_matchwin())
                break

            else:
                system_clear()
                show_scoreboard(time1, time2)
                print(result)
                print("O placar será resetado para o próximo set.")
                input("Pressione Enter para continuar...")
                match.reset()
    user_choice = input("Pressione Enter para reiniciar o programa ou 'q' para sair...").lower()
    if user_choice == 'q':
        print("Obrigado por usar o Volleyball Scoreboard!")
    else:
        system_clear()
        main()
if __name__ == "__main__":
    main()