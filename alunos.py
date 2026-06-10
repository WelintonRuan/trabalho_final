from mysql.connector import Error
import bcrypt
from database import criar_conexao
from utils import verificar_login_existente


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

                if idade <= 0 and idade > 100:
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

        if verificar_login_existente(login_aluno):
            print("Login já existe.")
            continue

        senha_aluno = input("Senha do aluno: ").strip()
        senha_hash = bcrypt.hashpw(
            senha_aluno.encode(),
            bcrypt.gensalt()
        ).decode()

        if not senha_aluno:
            print("Senha não pode ser vazia.")
            continue

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
                    (login_aluno, senha_hash, "ALUNO")
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

            cursor.execute(
                """
                SELECT id, nome, idade, turma
                FROM alunos
                ORDER BY nome
                """
            )

            alunos = cursor.fetchall()

            if not alunos:
                print("Nenhum aluno cadastrado.")
                return False

            print(f"{'ID':<5}{'Nome':<20}{'Idade':<10}{'Turma'}")
            print("-" * 45)

            for aluno in alunos:
                print(
                    f"{aluno[0]:<5}"
                    f"{aluno[1]:<20}"
                    f"{aluno[2]:<10}"
                    f"{aluno[3]}"
                )

            return True

        except Error as e:

            print(f"Erro: {e}")
            return False

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

    confirma = input("Tem certeza? (s/n): ").lower()

    if confirma != "s":
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

    if not listar_alunos():
        return

    conn = criar_conexao()

    if conn:

        cursor = conn.cursor()

        try:

            aluno_id = int(input("ID do aluno: "))

            cursor.execute(
                """
                SELECT id
                FROM alunos
                WHERE id = %s
                """,
                (aluno_id,)
            )

            if cursor.fetchone() is None:
                print("Aluno não encontrado.")
                return

            while True:

                try:

                    nova_turma = int(input("Nova turma: "))

                    if nova_turma <= 0:
                        print("Digite uma turma válida.")
                        continue

                    break

                except ValueError:
                    print("Digite apenas números.")

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

        except ValueError:

            print("Digite apenas números.")

        except Error as e:

            print(f"Erro: {e}")

        finally:

            cursor.close()
            conn.close()


def alterar_nome_aluno():

    if not listar_alunos():
        return

    conn = criar_conexao()

    if conn:

        cursor = conn.cursor()

        try:

            aluno_id = int(input("ID do aluno: "))

            cursor.execute(
                """
                SELECT id
                FROM alunos
                WHERE id = %s
                """,
                (aluno_id,)
            )

            if cursor.fetchone() is None:
                print("Aluno não encontrado.")
                return

            novo_nome = input("Novo nome: ").strip()

            if not novo_nome:
                print("Nome inválido.")
                return

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

        except ValueError:

            print("Digite apenas números.")

        except Error as e:

            print(f"Erro: {e}")

        finally:

            cursor.close()
            conn.close()



def buscar_aluno():

    busca = input(
        "Digite o ID ou nome do aluno: "
    ).strip()

    conn = criar_conexao()

    if not conn:
        return None

    cursor = conn.cursor()

    try:

        if busca.isdigit():

            cursor.execute(
                """
                SELECT id, nome, turma
                FROM alunos
                WHERE id = %s
                """,
                (int(busca),)
            )

        else:

            cursor.execute(
                """
                SELECT id, nome, turma
                FROM alunos
                WHERE nome LIKE %s
                """,
                (f"%{busca}%",)
            )

        resultados = cursor.fetchall()

        if not resultados:
            print("Aluno não encontrado.")
            return None

        if len(resultados) == 1:

            aluno_id = resultados[0][0]
            nome_aluno = resultados[0][1]
            turma_aluno = resultados[0][2]

        else:

            print("\nAlunos encontrados:\n")

            for aluno in resultados:

                print(
                    f"ID: {aluno[0]} | "
                    f"Nome: {aluno[1]} | "
                    f"Turma: {aluno[2]}"
                )

            while True:

                try:

                    aluno_id = int(
                        input(
                            "\nDigite o ID do aluno: "
                        )
                    )

                    ids_validos = [
                        aluno[0]
                        for aluno in resultados
                    ]

                    if aluno_id not in ids_validos:
                        print("ID inválido.")
                        continue

                    break

                except ValueError:

                    print("Digite apenas números.")

            aluno_selecionado = next(
                aluno
                for aluno in resultados
                if aluno[0] == aluno_id
            )

            nome_aluno = aluno_selecionado[1]
            turma_aluno = aluno_selecionado[2]

        print(
            f"\nAluno selecionado: "
            f"{nome_aluno} | "
            f"Turma: {turma_aluno}"
        )

        return aluno_id

    except Error as e:

        print(f"Erro: {e}")
        return None

    finally:

        cursor.close()
        conn.close()

