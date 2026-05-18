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
                    menu_prof(usuario)

                elif cargo == "ALUNO":
                    menu_aluno()

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
            break

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
    print("Área do aluno em construção.")


def cadastrar_professor():
    while True:
        try:
            print("\n--- Cadastrar Professor ---")

            nome = input("Nome do professor: ").strip()
            materia = input("Matéria: ").strip().lower()

            login_prof = input("Login do professor: ").strip()
            senha_prof = input("Senha do professor: ").strip()

            if not nome or not materia:
                print("Preencha todos os campos.")
                continue

            elif not nome.replace(" ","").isalpha:
                print("Seu nome nao tem como ter números.")
                continue

            elif len(senha_prof) < 8:
                print("A senha deve ter no minimo 8 caracteres.")
                continue

        except Error as e:
            print("Faça o que se pede.")
            continue

        conn = criar_conexao()

        if conn:

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    INSERT INTO professores (nome, materia)
                    VALUES (%s, %s)
                    """,
                    (login_prof, materia)
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
    while True:
        print("\n--- Cadastrar Aluno ---")

        nome = input("Nome do aluno: ").strip()

        if not nome:
            print("Nome não pode ser vazio.")
            continue

        while True:

            try:

                idade = int(input("Idade: "))

                if idade <= 0:
                    print("Digite uma idade válida.")
                    continue

                break

            except ValueError:
                print("Digite apenas números.")

        while True:

            try:

                turma = int(input("Turma: "))

                if turma <= 0:
                    print("Digite uma turma válida.")
                    continue

                break

            except ValueError:
                print("Digite apenas números.")

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

                aluno_id = cursor.lastrowid

                cursor.execute(
                    """
                    INSERT INTO usuarios (login, senha, cargo)
                    VALUES (%s, %s, %s)
                    """,
                    (login_aluno, senha_aluno, "ALUNO")
                )

                cursor.execute(
                    """
                    INSERT INTO notas (aluno_id)
                    VALUES (%s)
                    """,
                    (aluno_id,)
                )

                conn.commit()

                print("Aluno cadastrado com sucesso!")

            except Error as e:
                print(f"Erro: {e}")

            finally:
                cursor.close()
                conn.close()


def buscar_materia_professor(usuario):

    conn = criar_conexao()

    if conn:

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                SELECT materia
                FROM professores
                WHERE nome = %s
                """,
                (usuario,)
            )

            resultado = cursor.fetchone()

            if resultado:
                return resultado[0]

        except Error as e:
            print(f"Erro: {e}")

        finally:
            cursor.close()
            conn.close()


def lancar_nota(usuario):

    materia = buscar_materia_professor(usuario)

    if not materia:
        return print("Matéria do professor não encontrada.")

    print(f"\n--- Lançar nota de {materia} ---")

    if not listar_alunos():
        return

    while True:

        try:

            id_aluno = int(input("ID do aluno: "))

            if id_aluno <= 0:
                print("Digite um ID válido.")
                continue

            break

        except ValueError:
            print("Digite apenas números.")

    while True:

        try:

            nota = float(input(f"Nota de {materia}: "))

            if nota < 0 or nota > 10:
                print("Digite nota entre 0 e 10.")
                continue

            break

        except ValueError:
            print("Digite apenas números.")

    conn = criar_conexao()

    if conn:

        cursor = conn.cursor()

        try:

            cursor.execute(
                f"""
                UPDATE notas
                SET {materia} = %s
                WHERE aluno_id = %s
                """,
                (nota, id_aluno)
            )

            conn.commit()

            calcular_media(id_aluno)

            print("Nota lançada com sucesso!")

        except Error as e:
            print(f"Erro: {e}")

        finally:
            cursor.close()
            conn.close()


def calcular_media(id_aluno):

    conn = criar_conexao()

    if conn:

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                SELECT matematica,
                       portugues,
                       ciencias,
                       geografia,
                       historia,
                       edf,
                       artes,
                       algoritmo
                FROM notas
                WHERE aluno_id = %s
                """,
                (id_aluno,)
            )

            notas = cursor.fetchone()

            notas_validas = [n for n in notas if n is not None]

            media = sum(notas_validas) / len(notas_validas)

            if media >= 7:
                situacao = "Aprovado"

            else:
                situacao = "Reprovado"

            cursor.execute(
                """
                UPDATE notas
                SET media = %s,
                    situacao = %s
                WHERE aluno_id = %s
                """,
                (media, situacao, id_aluno)
            )

            conn.commit()

        except Error as e:
            print(f"Erro: {e}")

        finally:
            cursor.close()
            conn.close()


def remover_professor():

    print("Remover professor")

    if not listar_professores():
        return

    while True:

        try:

            id_professor = int(input("Id do professor para removelo: "))

            if id_professor <= 0:
                print("Digite um ID válido.")
                continue

            break

        except ValueError:
            print("Digite apenas números.")

    confirma = input(
        "Tem certeza? (s/n): "
    )

    if confirma.lower() != 's':
        return print("Operação cancelada.")

    conn = criar_conexao()

    if conn:

        cursor = conn.cursor()

        try:

            cursor.execute(
                "DELETE FROM professores WHERE id_professor = %s",
                (id_professor,)
            )

            conn.commit()

            print("Professor removido com sucesso!")

        except Error as e:
            print(f"Erro: {e}")

        finally:
            cursor.close()
            conn.close()


def listar_professores():

    print("\n--- Professores ---")

    conn = criar_conexao()

    if conn:

        cursor = conn.cursor()

        try:

            cursor.execute(
                "SELECT id_professor, nome, materia FROM professores ORDER BY nome"
            )

            professores = cursor.fetchall()

            if not professores:
                print("Nenhum professor cadastrado.")
                return False

            else:

                print(f"{'ID':<3} {'Nome':<15} {'Materia'}")
                print("-" * 45)

                for a in professores:
                    print(f"{a[0]:<3} {a[1]:<15} {a[2]}")

                return True

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
                "SELECT id, nome, idade, turma FROM alunos ORDER BY nome"
            )

            alunos = cursor.fetchall()

            if not alunos:
                print("Nenhum aluno cadastrado.")
                return False

            else:

                print(f"{'ID':<3} {'Nome':<15} {'Idade':<6} {'Turma'}")
                print("-" * 45)

                for a in alunos:
                    print(f"{a[0]:<3} {a[1]:<15} {a[2]:<6} {a[3]}")

                return True

        except Error as e:
            print(f"Erro: {e}")

        finally:
            cursor.close()
            conn.close()


def remover_aluno():

    print("Remover aluno")

    if not listar_alunos():
        return

    while True:

        try:

            id_aluno = int(input("Id do aluno para removelo: "))

            if id_aluno <= 0:
                print("Digite um ID válido.")
                continue

            break

        except ValueError:
            print("Digite apenas números.")

    confirma = input(
        "Tem certeza? (s/n): "
    )

    if confirma.lower() != 's':
        return print("Operação cancelada.")

    conn = criar_conexao()

    if conn:

        cursor = conn.cursor()

        try:

            cursor.execute(
                "DELETE FROM alunos WHERE id = %s",
                (id_aluno,)
            )

            conn.commit()

            print("Aluno removido com sucesso!")

        except Error as e:
            print(f"Erro: {e}")

        finally:
            cursor.close()
            conn.close()
login()