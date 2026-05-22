from binascii import Error

from database import criar_conexao


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

def listar_alunos():
    print("\n--- Lista de Alunos ---")
    conn = criar_conexao()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, nome, idade, turma FROM alunos ORDER BY nome")

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

def alterar_turma_aluno():
    listar_alunos()

    conn = criar_conexao()
    if conn:
        cursor = conn.cursor()

        try:
            aluno_id = int(input("ID do aluno: "))

            cursor.execute(
                "SELECT id FROM alunos WHERE id = %s",
                (aluno_id,)
            )

            if cursor.fetchone() is None:
                print("Aluno não encontrado.")
                return

            nova_turma = int(input("Nova turma: "))

            cursor.execute(
                """
                UPDATE alunos
                SET turma = %s
                WHERE id = %s
                """,
                (nova_turma, aluno_id)
            )

            conn.commit()
            print("Turma alterada com sucesso!")

        except Exception as e:
            print(f"Erro: {e}")

        finally:
            cursor.close()
            conn.close()

def alterar_nome_aluno():
    listar_alunos()

    conn = criar_conexao()
    if conn:
        cursor = conn.cursor()

        try:
            aluno_id = int(input("ID do aluno: "))

            cursor.execute(
                "SELECT id FROM alunos WHERE id = %s",
                (aluno_id,)
            )

            if cursor.fetchone() is None:
                print("Aluno não encontrado.")
                return

            novo_nome = input("Novo nome: ")

            cursor.execute(
                """
                UPDATE alunos
                SET nome = %s
                WHERE id = %s
                """,
                (novo_nome, aluno_id)
            )

            conn.commit()
            print("Nome alterado com sucesso!")

        except Exception as e:
            print(f"Erro: {e}")

        finally:
            cursor.close()
            conn.close()