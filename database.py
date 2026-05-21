import mysql.connector
from mysql.connector import Error
import os
global conexao_global


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