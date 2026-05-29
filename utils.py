from mysql.connector import Error
from database import criar_conexao


def verificar_materia_existente(materia):

    conn = criar_conexao()

    if not conn:
        return False

    cursor = conn.cursor()

    try:

        sql = """
        SELECT id, nome
        FROM professores
        WHERE materia = %s
        """

        cursor.execute(sql, (materia,))

        resultado = cursor.fetchone()

        if resultado:
            print(f"Professor atual: {resultado[1]} (ID: {resultado[0]})")
            return True

        return False

    except Error as e:

        print(f"Erro ao verificar matéria: {e}")
        return False

    finally:

        cursor.close()
        conn.close()


def verificar_login_existente(login):

    conn = criar_conexao()

    if not conn:
        return False

    cursor = conn.cursor()

    try:

        sql = """
        SELECT id
        FROM usuarios
        WHERE login = %s
        """

        cursor.execute(sql, (login,))

        return cursor.fetchone() is not None

    except Error as e:

        print(f"Erro ao verificar login: {e}")
        return False

    finally:

        cursor.close()
        conn.close()