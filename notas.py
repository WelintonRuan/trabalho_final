from binascii import Error

from alunos import listar_alunos
from database import criar_conexao
from professor import buscar_materia_professor



def lancar_nota(usuario):

    materia = buscar_materia_professor(usuario)

    if not materia:
        print("Matéria do professor não encontrada.")
        return

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
                """
                SELECT aluno_id
                FROM notas
                WHERE aluno_id = %s
                """,
                (id_aluno,)
            )

            existe = cursor.fetchone()

            if not existe:

                cursor.execute(
                    """
                    INSERT INTO notas (aluno_id)
                    VALUES (%s)
                    """,
                    (id_aluno,)
                )

            cursor.execute(
                f"""
                UPDATE notas
                SET {materia} = %s
                WHERE aluno_id = %s
                """,
                (nota, id_aluno)
            )

            if cursor.rowcount == 0:
                print("Erro ao lançar nota.")
                return

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
                """,(id_aluno,))

            notas = cursor.fetchone()

            if notas is None:
                print("Aluno não possui registro de notas.")
                return

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
                """,(media, situacao, id_aluno))

            conn.commit()

        except Error as e:
            print(f"Erro: {e}")

        finally:
            cursor.close()
            conn.close()

def ver_nota(materia):
    conn = criar_conexao()
    if conn:
        cursor = conn.cursor()
        try:

            sql = f"""
            SELECT aluno_id, {materia}
            FROM notas
            """

            cursor.execute(sql)

            notas = cursor.fetchall()

            if not notas:
                print("Nenhuma nota encontrada.")
                return

            print(f"\n--- Nota de {materia} ---")
            print(f"{'Aluno ID':<10} {'Nota'}")
            print("-" * 20)

            for nota in notas:
                print(f"{nota[0]:<10} {nota[1]}")

        except Error as e:
            print(f"Erro: {e}")

        finally:
            cursor.close()
            conn.close()