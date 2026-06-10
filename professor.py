from mysql.connector import Error
import bcrypt
from database import criar_conexao
from utils import verificar_login_existente


def listar_professores():

    print("\n--- Professores ---")

    conn = criar_conexao()

    if conn:

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                SELECT id, nome, materia
                FROM professores
                ORDER BY nome
                """
            )

            professores = cursor.fetchall()

            if not professores:
                print("Nenhum professor cadastrado.")
                return False

            print(f"{'ID':<5}{'Nome':<20}{'Matéria'}")
            print("-" * 45)

            for professor in professores:
                print(
                    f"{professor[0]:<5}"
                    f"{professor[1]:<20}"
                    f"{professor[2]}"
                )

            return True

        except Error as e:

            print(f"Erro: {e}")
            return False

        finally:

            cursor.close()
            conn.close()


def remover_professor():

    print("\n--- Remover professor ---")

    if not listar_professores():
        return

    while True:

        try:

            id_professor = int(input("ID do professor para remover: "))

            if id_professor <= 0:
                print("Digite um ID válido.")
                continue

            break

        except ValueError:
            print("Digite apenas números.")

    confirma = input("Tem certeza? (s/n): ").strip().lower()

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
                FROM professores
                WHERE id = %s
                """,
                (id_professor,)
            )

            professor = cursor.fetchone()

            if not professor:
                print("Professor não encontrado.")
                return

            login_prof = professor[0]

            cursor.execute(
                """
                DELETE FROM professores
                WHERE id = %s
                """,
                (id_professor,)
            )

            cursor.execute(
                """
                DELETE FROM usuarios
                WHERE login = %s
                """,
                (login_prof,)
            )

            conn.commit()

            print("Professor removido com sucesso!")

        except Error as e:

            conn.rollback()
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
                WHERE login = %s
                """,
                (usuario,)
            )

            resultado = cursor.fetchone()

            if resultado:
                return resultado[0]

            return None

        except Error as e:

            print(f"Erro: {e}")
            return None

        finally:

            cursor.close()
            conn.close()


def cadastrar_professor():

    materias_validas = [
        "matematica",
        "portugues",
        "ciencias",
        "geografia",
        "historia",
        "edf",
        "artes",
        "algoritmo"
    ]

    while True:

        print("\n--- Cadastrar Professor ---")

        nome = input("Nome do professor: ").strip()

        materia = input("Matéria: ").strip().lower()

        login_prof = input("Login do professor: ").strip()

        senha_prof = input("Senha do professor: ").strip()
        senha_prof_hash = bcrypt.hashpw(
            senha_prof.encode(),
            bcrypt.gensalt()
        ).decode()

        if not nome or not materia or not login_prof or not senha_prof:
            print("Preencha todos os campos.")
            continue

        if materia not in materias_validas:
            print("Matéria inválida.")
            continue

        if verificar_login_existente(login_prof):
            print("Login já existe.")
            continue

        conn = criar_conexao()

        if conn:

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    INSERT INTO professores (nome, materia, login)
                    VALUES (%s, %s, %s)
                    """,
                    (nome, materia, login_prof)
                )

                cursor.execute(
                    """
                    INSERT INTO usuarios (login, senha, cargo)
                    VALUES (%s, %s, %s)
                    """,
                    (login_prof, senha_prof_hash, "PROF")
                )

                conn.commit()

                print("Professor cadastrado com sucesso!")
                return

            except Error as e:

                conn.rollback()
                print(f"Erro: {e}")

            finally:

                cursor.close()
                conn.close()


def deletar_professor_por_materia(materia):

    conn = criar_conexao()

    if not conn:
        return False

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            SELECT id
            FROM professores
            WHERE materia = %s
            """,
            (materia,)
        )

        professor = cursor.fetchone()

        if not professor:
            return False

        professor_id = professor[0]

        cursor.execute(
            """
            DELETE FROM professores
            WHERE id = %s
            """,
            (professor_id,)
        )

        conn.commit()

        return True

    except Error as e:

        print(f"Erro ao deletar professor: {e}")
        conn.rollback()
        return False

    finally:

        cursor.close()
        conn.close()


def alterar_nome_professor():

    if not listar_professores():
        return

    conn = criar_conexao()

    if conn:

        cursor = conn.cursor()

        try:

            professor_id = int(input("ID do professor: "))

            cursor.execute(
                """
                SELECT id
                FROM professores
                WHERE id = %s
                """,
                (professor_id,)
            )

            if cursor.fetchone() is None:
                print("Professor não encontrado.")
                return

            novo_nome = input("Novo nome: ").strip()

            if not novo_nome:
                print("Nome inválido.")
                return

            cursor.execute(
                """
                UPDATE professores
                SET nome = %s
                WHERE id = %s
                """,
                (novo_nome, professor_id)
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


def alterar_materia_professor():

    if not listar_professores():
        return

    materias_validas = [
        "matematica",
        "portugues",
        "ciencias",
        "geografia",
        "historia",
        "edf",
        "artes",
        "algoritmo"
    ]

    conn = criar_conexao()

    if conn:

        cursor = conn.cursor()

        try:

            professor_id = int(input("ID do professor: "))

            cursor.execute(
                """
                SELECT id
                FROM professores
                WHERE id = %s
                """,
                (professor_id,)
            )

            if cursor.fetchone() is None:
                print("Professor não encontrado.")
                return

            nova_materia = input("Nova matéria: ").strip().lower()

            if nova_materia not in materias_validas:
                print("Matéria inválida.")
                return

            cursor.execute(
                """
                UPDATE professores
                SET materia = %s
                WHERE id = %s
                """,
                (nova_materia, professor_id)
            )

            conn.commit()

            print("Matéria alterada com sucesso!")

        except ValueError:

            print("Digite apenas números.")

        except Error as e:

            print(f"Erro: {e}")

        finally:

            cursor.close()
            conn.close()