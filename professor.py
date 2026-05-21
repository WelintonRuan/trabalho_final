from binascii import Error

from database import criar_conexao
from database import listar_professores, verificar_login_existente


def cadastrar_professor():

    global conexao_global

    while True:

        print("\n--- Cadastrar Professor ---")

        materias_validas = [
            "matematica",
            "portugues",
            "ciencias",
            "geografia",
            "historia",
            "educacao fisica",
            "artes",
            "algoritmo"
        ]

        nome = input("Nome do professor: ").strip()
        materia = input("Matéria: ").strip().lower()
        login_prof = input("Login do professor: ").strip()
        senha_prof = input("Senha do professor: ").strip()

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
                    (login_prof, senha_prof, "PROF")
                )

                conn.commit()

                print("Professor cadastrado com sucesso!")

                break

            except Error as e:

                conn.rollback()
                print(f"Erro: {e}")

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


def listar_professores():
    print("\n--- Professores ---")
    conn = criar_conexao()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, nome, materia FROM professores ORDER BY nome")

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

        finally:
            cursor.close()
            conn.close()


def deletar_professor_por_materia(materia):
    global conexao_global
    cursor = None
    try:
        cursor = conexao_global.cursor()
        cursor.execute("SELECT id FROM professores WHERE materia = %s", (materia,))
        professor = cursor.fetchone()
        
        if professor:
            professor_id = professor[0]

            cursor.execute("DELETE FROM professores WHERE id = %s", (professor_id,))
            conexao_global.commit()
            return True
        return False
        
    except Error as e:
        print(f" Erro ao deletar professor: {e}")
        conexao_global.rollback()
        return False
    finally:
        if cursor:
            cursor.close()