from mysql.connector import Error

from alunos import listar_alunos
from database import criar_conexao
from professor import buscar_materia_professor


def calcular_media_trimestre(n1, n2, n3):
    return round((n1 + n2 + n3) / 3, 2)


def calcular_media_final(aluno_id, materia):

    conn = criar_conexao()

    if not conn:
        return

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            SELECT media_trimestre
            FROM notas
            WHERE aluno_id = %s
            AND materia = %s
            ORDER BY trimestre
            """,
            (aluno_id, materia)
        )

        medias = cursor.fetchall()

        if len(medias) < 3:
            return

        media_final = round(
            sum(m[0] for m in medias) / 3,
            2
        )

        situacao = (
            "Aprovado"
            if media_final >= 7
            else "Reprovado"
        )

        cursor.execute(
            """
            INSERT INTO medias_finais
            (
                aluno_id,
                materia,
                media_final,
                situacao
            )
            VALUES (%s,%s,%s,%s)

            ON DUPLICATE KEY UPDATE
                media_final = VALUES(media_final),
                situacao = VALUES(situacao)
            """,
            (
                aluno_id,
                materia,
                media_final,
                situacao
            )
        )

        conn.commit()

    except Error as e:

        print(f"Erro: {e}")

    finally:

        cursor.close()
        conn.close()


def lancar_notas(usuario):

    materia = buscar_materia_professor(usuario)

    if not materia:
        print("Matéria do professor não encontrada.")
        return

    print(f"\n===== {materia.upper()} =====")

    if not listar_alunos():
        return

    try:

        aluno_id = int(input("ID do aluno: "))

        trimestre = int(input("Trimestre (1-3): "))

        if trimestre not in [1, 2, 3]:
            print("Trimestre inválido.")
            return

        n1 = float(input("Nota 1: "))
        n2 = float(input("Nota 2: "))
        n3 = float(input("Nota 3: "))

        for nota in [n1, n2, n3]:

            if nota < 0 or nota > 10:
                print("Notas devem estar entre 0 e 10.")
                return

        media = calcular_media_trimestre(
            n1,
            n2,
            n3
        )

        conn = criar_conexao()

        if not conn:
            return

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO notas
                (
                    aluno_id,
                    materia,
                    trimestre,
                    nota1,
                    nota2,
                    nota3,
                    media_trimestre
                )
                VALUES
                (%s,%s,%s,%s,%s,%s,%s)

                ON DUPLICATE KEY UPDATE
                    nota1 = VALUES(nota1),
                    nota2 = VALUES(nota2),
                    nota3 = VALUES(nota3),
                    media_trimestre = VALUES(media_trimestre)
                """,
                (
                    aluno_id,
                    materia,
                    trimestre,
                    n1,
                    n2,
                    n3,
                    media
                )
            )

            conn.commit()

            calcular_media_final(
                aluno_id,
                materia
            )

            print(
                f"Média do {trimestre}º trimestre: {media}"
            )

            print("Notas lançadas com sucesso!")

        except Error as e:

            print(f"Erro: {e}")

        finally:

            cursor.close()
            conn.close()

    except ValueError:

        print("Digite apenas números.")


def ver_boletim(usuario):

    conn = criar_conexao()

    if not conn:
        return

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            SELECT id,nome
            FROM alunos
            WHERE login = %s
            """,
            (usuario,)
        )

        aluno = cursor.fetchone()

        if not aluno:
            print("Aluno não encontrado.")
            return

        aluno_id = aluno[0]
        nome = aluno[1]

        print("\n===== BOLETIM =====")
        print(f"Aluno: {nome}")

        cursor.execute(
            """
            SELECT DISTINCT materia
            FROM notas
            WHERE aluno_id = %s
            ORDER BY materia
            """,
            (aluno_id,)
        )

        materias = cursor.fetchall()

        if not materias:
            print("Nenhuma nota cadastrada.")
            return

        for materia in materias:

            materia_nome = materia[0]

            print("\n--------------------------")
            print(f"Matéria: {materia_nome}")
            print("--------------------------")

            cursor.execute(
                """
                SELECT
                    trimestre,
                    nota1,
                    nota2,
                    nota3,
                    media_trimestre
                FROM notas
                WHERE aluno_id = %s
                AND materia = %s
                ORDER BY trimestre
                """,
                (
                    aluno_id,
                    materia_nome
                )
            )

            trimestres = cursor.fetchall()

            for t in trimestres:

                print(f"\n{t[0]}º Trimestre")

                print(f"Nota 1: {t[1]}")
                print(f"Nota 2: {t[2]}")
                print(f"Nota 3: {t[3]}")
                print(f"Média: {t[4]}")

            cursor.execute(
                """
                SELECT
                    media_final,
                    situacao
                FROM medias_finais
                WHERE aluno_id = %s
                AND materia = %s
                """,
                (
                    aluno_id,
                    materia_nome
                )
            )

            resultado = cursor.fetchone()

            if resultado:

                print(
                    f"\nMédia Final: {resultado[0]}"
                )

                print(
                    f"Situação: {resultado[1]}"
                )

    except Error as e:

        print(f"Erro: {e}")

    finally:

        cursor.close()
        conn.close()