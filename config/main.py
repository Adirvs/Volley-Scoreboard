from match import Match
from team import Time
import os


def system_clear():
    os.system('cls')


def show_scoreboard(time1, time2):
    print(f"\nPlacar: {time1.nome} {time1.score} x {time2.score} {time2.nome}")
    print(f"Sets: {time1.nome} {time1.set} x {time2.set} {time2.nome}")


def setup():
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
                print("O placar será resetado para o próximo set.")
                input("Pressione Enter para continuar...")
                match.reset()
main()