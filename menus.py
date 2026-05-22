from binascii import Error

from alunos import alterar_nome_aluno, alterar_turma_aluno, cadastrar_aluno, listar_alunos,remover_aluno
from database import criar_conexao
from professor import alterar_materia_professor, alterar_nome_professor, cadastrar_professor,listar_professores,remover_professor
from notas import lancar_nota,ver_nota

def login():
    print("\n========= LOGIN =========")

    global conexao_global

    usuario = input("Usuário: ")
    senha = input("Senha: ")

    conn = criar_conexao()
    conexao_global = conn

    if conn:

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

            if resultado:

                cargo = resultado[0]

                print("\nLogin realizado com sucesso!")

                if cargo == "ADM":
                    menu_adm()

                elif cargo == "PROF":
                    menu_prof(usuario)

                elif cargo == "ALUNO":
                    menu_aluno()

            else:
                print("Usuário ou senha incorretos.")
                menu_login()

        except Error as e:
            print(f"Erro: {e}")

        finally:
            cursor.close()


def menu_adm():

    while True:

        print("\n========= MENU ADM =========")
        print("1 - Administrar professor")
        print("2 - Administrar aluno")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            menu_administrar_professor()

        elif opcao == "2":
            menu_administrar_alunos()
       

        elif opcao == "0":
            menu_login()

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
            menu_login()

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
            menu_login()

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

def menu_login():
    print("1- logar")
    print("0- Sair")

    opcao = input("Escolha: ")

    if opcao == "1":
        login()

    elif opcao == "0":
        exit()
    
    else:
        print("Escolha uma opçao valida")
        menu_login()


def menu_administrar_professor():
    print("1 - Cadastrar professor")
    print("2 - Remover professor")
    print("3 - Listar professor")
    print("4 - Mudar materia")
    print("5 - Mudar nome")
    print("0 - Sair")

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
        return
    
    else:
        print("Escolha uma opçao valida")
        menu_administrar_professor()


def menu_administrar_alunos():
    print("1 - Cadastrar alunos")
    print("2 - Remover alunos")
    print("3 - Listar alunos")
    print("4 - Mudar turma dos alunos")
    print("5 - Mudar nome dos alunos")
    print("0 - Sair")

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
        return

    else:
        print("Escolha uma opçao valida")
        menu_administrar_alunos()
