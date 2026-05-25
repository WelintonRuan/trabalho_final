from mysql.connector import Error

from alunos import (
    cadastrar_aluno,
    listar_alunos,
    remover_aluno,
    alterar_turma_aluno,
    alterar_nome_aluno
)

from professor import (
    cadastrar_professor,
    listar_professores,
    remover_professor,
    alterar_materia_professor,
    alterar_nome_professor
)

from notas import lancar_nota, ver_nota
from database import criar_conexao


def login():

    print("\n========= LOGIN =========")

    usuario = input("Usuário: ")
    senha = input("Senha: ")

    conn = criar_conexao()

    if not conn:
        return

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            SELECT cargo
            FROM usuarios
            WHERE login = %s AND senha = %s
            """,
            (usuario, senha)
        )

        resultado = cursor.fetchone()

        if not resultado:
            print("Usuário ou senha incorretos.")
            return

        cargo = resultado[0]

        print("\nLogin realizado com sucesso!")

        if cargo == "ADM":
            menu_adm()

        elif cargo == "PROF":
            menu_prof(usuario)

        elif cargo == "ALUNO":
            menu_aluno(usuario)

    except Error as e:

        print(f"Erro: {e}")

    finally:

        cursor.close()
        conn.close()


def menu_login():

    while True:

        print("\n========= SISTEMA ESCOLAR =========")
        print("1 - Logar")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":

            login()

        elif opcao == "0":

            print("Sistema encerrado.")
            break

        else:

            print("Escolha uma opção válida.")


def menu_adm():

    while True:

        print("\n========= MENU ADM =========")
        print("1 - Administrar professores")
        print("2 - Administrar alunos")
        print("0 - Logout")

        opcao = input("Escolha: ")

        if opcao == "1":

            menu_administrar_professor()

        elif opcao == "2":

            menu_administrar_alunos()

        elif opcao == "0":

            break

        else:

            print("Opção inválida.")


def menu_prof(usuario):

    while True:

        print("\n========= MENU PROFESSOR =========")
        print("1 - Lançar nota")
        print("2 - Listar alunos")
        print("0 - Logout")

        opcao = input("Escolha: ")

        if opcao == "1":

            lancar_nota(usuario)

        elif opcao == "2":

            listar_alunos()

        elif opcao == "0":

            break

        else:

            print("Opção inválida.")


def menu_aluno(usuario):

    while True:

        print("\n========= MENU ALUNO =========")
        print("1 - Ver notas")
        print("0 - Logout")

        opcao = input("Escolha: ")

        if opcao == "1":

            menu_notas(usuario)

        elif opcao == "0":

            break

        else:

            print("Opção inválida.")


def menu_notas(usuario):

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

            ver_nota(usuario, "matematica")

        elif opcao == "2":

            ver_nota(usuario, "portugues")

        elif opcao == "3":

            ver_nota(usuario, "ciencias")

        elif opcao == "4":

            ver_nota(usuario, "geografia")

        elif opcao == "5":

            ver_nota(usuario, "historia")

        elif opcao == "6":

            ver_nota(usuario, "edf")

        elif opcao == "7":

            ver_nota(usuario, "artes")

        elif opcao == "8":

            ver_nota(usuario, "algoritmo")

        elif opcao == "0":

            break

        else:

            print("Opção inválida.")


def menu_administrar_professor():

    while True:

        print("\n===== ADMINISTRAR PROFESSORES =====")
        print("1 - Cadastrar professor")
        print("2 - Remover professor")
        print("3 - Listar professores")
        print("4 - Alterar matéria")
        print("5 - Alterar nome")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":

            cadastrar_professor()

        elif opcao == "2":

            remover_professor()

        elif opcao == "3":

            listar_professores()

        elif opcao == "4":

            alterar_materia_professor()

        elif opcao == "5":

            alterar_nome_professor()

        elif opcao == "0":

            break

        else:

            print("Opção inválida.")


def menu_administrar_alunos():

    while True:

        print("\n===== ADMINISTRAR ALUNOS =====")
        print("1 - Cadastrar aluno")
        print("2 - Remover aluno")
        print("3 - Listar alunos")
        print("4 - Alterar turma")
        print("5 - Alterar nome")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":

            cadastrar_aluno()

        elif opcao == "2":

            remover_aluno()

        elif opcao == "3":

            listar_alunos()

        elif opcao == "4":

            alterar_turma_aluno()

        elif opcao == "5":

            alterar_nome_aluno()

        elif opcao == "0":

            break

        else:

            print("Opção inválida.")