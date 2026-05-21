from binascii import Error

from database import criar_conexao
from database import listar_alunos


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
                    INSERT INTO alunos (nome, idade, turma, login)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (nome, idade, turma, login_aluno)
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

                return

            except Error as e:

                conn.rollback()
                print(f"Erro: {e}")

            finally:
                cursor.close()
                conn.close()


def remover_aluno():

    print("\n--- Remover aluno ---")

    if not listar_alunos():
        return

    while True:

        try:

            id_aluno = int(input("ID do aluno para remover: "))

            if id_aluno <= 0:
                print("Digite um ID válido.")
                continue

            break

        except ValueError:
            print("Digite apenas números.")

    confirma = input("Tem certeza? (s/n): ")

    if confirma.lower() != "s":
        print("Operação cancelada.")
        return

    conn = criar_conexao()

    if conn:

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                SELECT login
                FROM alunos
                WHERE id = %s
                """,
                (id_aluno,)
            )

            aluno = cursor.fetchone()

            if not aluno:
                print("Aluno não encontrado.")
                return

            login_aluno = aluno[0]

            cursor.execute(
                """
                DELETE FROM notas
                WHERE aluno_id = %s
                """,
                (id_aluno,)
            )

            cursor.execute(
                """
                DELETE FROM alunos
                WHERE id = %s
                """,
                (id_aluno,)
            )

            cursor.execute(
                """
                DELETE FROM usuarios
                WHERE login = %s
                """,
                (login_aluno,)
            )

            conn.commit()

            print("Aluno removido com sucesso!")

        except Error as e:

            conn.rollback()
            print(f"Erro: {e}")

        finally:
            cursor.close()
            conn.close()

