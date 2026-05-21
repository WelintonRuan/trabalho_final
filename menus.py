from database import cadastrar_aluno, cadastrar_professor, lancar_nota, listar_alunos, listar_professores, menu_notas, remover_aluno, remover_professor, ver_nota


def menu_adm():

    while True:

        print("\n========= MENU ADM =========")
        print("1 - Cadastrar professor")
        print("2 - Cadastrar aluno")
        print("3 - Remover professor")
        print("4 - Remover aluno")
        print("5 - Listar professores")
        print("6 - Listar alunos")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_professor()

        elif opcao == "2":
            cadastrar_aluno()

        elif opcao == "3":
            remover_professor()

        elif opcao == "4":
            remover_aluno()

        elif opcao == "5":
            listar_professores()

        elif opcao == "6":
            listar_alunos()

        elif opcao == "0":
            return

        else:
            print("Opção inválida.")

def menu_prof(usuario):

    while True:

        print("\n========= MENU PROF =========")
        print("1 - Lançar nota")
        print("2 - Ver alunos")
        print("0 - Sair")

        menu = input("Escolha: ")

        if menu == "1":
            lancar_nota(usuario)

        elif menu == "2":
            listar_alunos()

        elif menu == "0":
            break

        else:
            print("Opção inválida.")


def menu_aluno():
    while True:
        print("\n========= MENU ALUNO =========")
        print("1 - Ver notas")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            menu_notas()

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")

def menu_notas():
    while True:
        print("\n========= NOTAS =========")
        print("1 - Matemática")
        print("2 - Português")
        print("3 - Ciências")
        print("4 - Geografia")
        print("5 - História")
        print("6 - Educação Física")
        print("7 - Artes")
        print("8 - Algoritmo")
        print("0 - Voltar")

        opcao = input("Escolha a matéria: ")

        if opcao == "1":
            ver_nota("matematica")

        elif opcao == "2":
            ver_nota("portugues")

        elif opcao == "3":
            ver_nota("ciencias")

        elif opcao == "4":
            ver_nota("geografia")

        elif opcao == "5":
            ver_nota("historia")

        elif opcao == "6":
            ver_nota("edf")

        elif opcao == "7":
            ver_nota("artes")

        elif opcao == "8":
            ver_nota("algoritmo")

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")