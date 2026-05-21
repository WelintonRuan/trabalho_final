from binascii import Error

from database import criar_conexao
from menus import menu_adm, menu_aluno, menu_prof

def login():
    print("\n========= LOGIN =========")

    global conexao_global

    usuario = input("Usuário: ")
    senha = input("Senha: ")

    conn = criar_conexao()
    conexao_global = conn

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

login()