import mysql.connector
from mysql.connector import Error
import os

def criar_conexao():
    try:
        return mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password=os.getenv("DB_PASSWORD", "Senac2026"),
            database='escola'
        )

    except Error as e:
        print(f"Erro ao conectar: {e}")
        return None


def login():
    print("\n========= LOGIN =========")
    usuario = input("Usuário: ")
    senha = input("Senha: ")

    conn = criar_conexao()

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
                    ...

                elif cargo == "ALUNO":
                    ...

            else:
                print("Usuário ou senha incorretos.")

        except Error as e:

            print(f"Erro: {e}")

        finally:

            cursor.close()
            conn.close()



def menu_adm():
    while True:
        print("\n========= MENU ADM =========")
        print("1 - Cadastrar professor")
        print("2 - Cadastrar aluno")
        print("3 - Remover professor")
        print("4 - Remover aluno")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_professor()

        elif opcao == "2":
            cadastrar_aluno()

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")


def cadastrar_professor():
    print("\n--- Cadastrar Professor ---")

    nome = input("Nome do professor: ").strip()
    materia = input("Matéria: ").strip()

    login_prof = input("Login do professor: ").strip()
    senha_prof = input("Senha do professor: ").strip()

    if not nome or not materia:
        return print("Preencha todos os campos.")

    conn = criar_conexao()

    if conn:

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO professores (nome, materia)
                VALUES (%s, %s)
                """,
                (nome, materia)
            )

            cursor.execute(
                """
                INSERT INTO usuarios (login, senha, cargo)
                VALUES (%s, %s, %s)
                """,
                (login_prof, senha_prof, "PROF")
            )

            conn.commit()

            print("Professor cadastrado com sucesso!")

        except Error as e:

            print(f"Erro: {e}")

        finally:

            cursor.close()
            conn.close()


def cadastrar_aluno():
    print("\n--- Cadastrar Aluno ---")

    nome = input("Nome do aluno: ").strip()

    if not nome:
        return print("Nome não pode ser vazio.")

    try:

        idade = int(input("Idade: "))
        turma = int(input("Turma: "))

    except ValueError:

        return print("Digite apenas números.")

    login_aluno = input("Login do aluno: ").strip()
    senha_aluno = input("Senha do aluno: ").strip()

    conn = criar_conexao()

    if conn:

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO alunos (nome, idade, turma)
                VALUES (%s, %s, %s)
                """,
                (nome, idade, turma)
            )

            cursor.execute(
                """
                INSERT INTO usuarios (login, senha, cargo)
                VALUES (%s, %s, %s)
                """,
                (login_aluno, senha_aluno, "ALUNO")
            )

            conn.commit()

            print("Aluno cadastrado com sucesso!")

        except Error as e:

            print(f"Erro: {e}")

        finally:

            cursor.close()
            conn.close()

def remover_professor():
    print("Remover professor")

    #ficaria para listar os professor

    try:
        id_professor = int(input("Id do professor para removelo: "))
    
    except ValueError:
        print("Erro id invalido")

    confirma = input(
        "Tem certeza? As notas também serão removidas. (s/n): ")
    
    if confirma.lower() != 's':
        return print("Operação cancelada.")

    conn = criar_conexao()
    if conn:
        cursor = conn.cursor()

        try:
            cursor.execute(
                "DELETE FROM professores WHERE id = %s",(id_professor,))
            conn.commit()
            print("Professor removido com sucesso!")

        except Error as e:
            print(f"Erro: {e}")

        finally:
            cursor.close()
            conn.close()


def listar_professores():
    print("\n--- Lista de Alunos ---")

    conn = criar_conexao()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT id, nome, materia FROM alunos ORDER BY nome")

            professores = cursor.fetchall()

            if not professores:
                print("Nenhum professor cadastrado.")

            else:
                print(f"{'ID':<3} {'Nome':<3} {'Materia':<3}")
                print("-" * 45)

                for a in professores:
                    print(f"{a[0]:<3} {a[1]:<3} {a[2]:<3}")

        except Error as e:
            print(f"Erro: {e}")

        finally:
            cursor.close()
            conn.close()

def listar_alunos():
    print("\n--- Lista de Alunos ---")

    conn = criar_conexao()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT id, nome, idade, turma FROM alunos ORDER BY nome")

            alunos = cursor.fetchall()

            if not alunos:
                print("Nenhum aluno cadastrado.")

            else:
                print(f"{'ID':<3} {'Nome':<3} {'Idade':<3} {'Turma'}")
                print("-" * 45)

                for a in alunos:
                    print(f"{a[0]:<3} {a[1]:<3} {a[2]:<3} {a[3]}")

        except Error as e:
            print(f"Erro: {e}")

        finally:
            cursor.close()
            conn.close()

def remover_aluno():
    print("Remover professor")

    listar_alunos()
    
    try:
        id_aluno = int(input("Id do professor para removelo: "))
    
    except ValueError:
        print("Erro id invalido")

    confirma = input(
        "Tem certeza? As notas também serão removidas. (s/n): ")
    
    if confirma.lower() != 's':
        return print("Operação cancelada.")

    conn = criar_conexao()
    if conn:
        cursor = conn.cursor()

        try:
            cursor.execute(
                "DELETE FROM alunos WHERE id = %s",(id_aluno,))
            conn.commit()
            print("Aluno removido com sucesso!")

        except Error as e:
            print(f"Erro: {e}")

        finally:
            cursor.close()
            conn.close()

