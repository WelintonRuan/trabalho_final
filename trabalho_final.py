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
                    ...

                elif cargo == "ALUNO":
                    ...

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
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            ...

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")