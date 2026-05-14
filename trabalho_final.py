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

def cadastrarAluno():
    print("Casdastrar alunos")

    nome = input("Coloque o nome do aluno: ").strip()

    if not nome:
        return print("Nome nao deve ser vazio")
    
    try:
        idade = int(input("Idade do aluno: "))
        turma = int(input("Turma do aluno: "))
    except ValueError as e:
        print("{e}")
