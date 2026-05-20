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


def menu_adm():

    while True:

        print("\n========= MENU ADM =========")
        print("1 - Cadastrar professor")
        print("2 - Cadastrar aluno")
        print("3 - Remover professor")
        print("4 - Remover aluno")
        print("5 - Listar professores")
        print("6 - Listar alunos")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_professor()

        elif opcao == "2":
            cadastrar_aluno()

        elif opcao == "3":
            remover_professor()

        elif opcao == "4":
            remover_aluno()

        elif opcao == "5":
            listar_professores()

        elif opcao == "6":
            listar_alunos()

        elif opcao == "0":
            return

        else:
            print("Opção inválida.")


def menu_prof(usuario):

    while True:

        print("\n========= MENU PROF =========")
        print("1 - Lançar nota")
        print("2 - Ver alunos")
        print("0 - Sair")

        menu = input("Escolha: ")

        if menu == "1":
            lancar_nota(usuario)

        elif menu == "2":
            listar_alunos()

        elif menu == "0":
            break

        else:
            print("Opção inválida.")


def menu_aluno():
    while True:
        print("\n========= MENU ALUNO =========")
        print("1 - Ver notas")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            menu_notas()

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")


def verificar_materia_existente(materia):
    global conexao_global
    cursor = None
    try:
        cursor = conexao_global.cursor()
        sql = "SELECT id, nome FROM professores WHERE materia = %s"
        cursor.execute(sql, (materia,))
        resultado = cursor.fetchone()
        
        if resultado:
            print(f"   Professor atual: {resultado[1]} (ID: {resultado[0]})")
            return True
        return False
        
    except Error as e:
        print(f"Erro ao verificar matéria: {e}")
        return False
    finally:
        if cursor:
            cursor.close()

def verificar_login_existente(login):
    global conexao_global
    cursor = None
    try:
        cursor = conexao_global.cursor()
        sql = "SELECT id FROM usuarios WHERE login = %s"
        cursor.execute(sql, (login,))
        return cursor.fetchone() is not None
        
    except Error as e:
        print(f"Erro ao verificar login: {e}")
        return False
    finally:
        if cursor:
            cursor.close()

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

                if idade <= 0:
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
        senha_aluno = input("Senha do aluno: ").strip()

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
                    (login_aluno, senha_aluno, "ALUNO")
                )

                cursor.execute(
                    """
                    INSERT INTO notas (aluno_id)
                    VALUES (%s)
                    """,
                    (aluno_id,)
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


def listar_alunos():
    print("\n--- Lista de Alunos ---")
    conn = criar_conexao()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, nome, idade, turma FROM alunos ORDER BY nome")

            alunos = cursor.fetchall()

            if not alunos:
                print("Nenhum aluno cadastrado.")
                return False

            else:

                print(f"{'ID':<3} {'Nome':<15} {'Idade':<6} {'Turma'}")
                print("-" * 45)

                for a in alunos:
                    print(f"{a[0]:<3} {a[1]:<15} {a[2]:<6} {a[3]}")

                return True

        except Error as e:
            print(f"Erro: {e}")

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

def menu_notas():
    while True:
        print("\n========= NOTAS =========")
        print("1 - Matemática")
        print("2 - Português")
        print("3 - Ciências")
        print("4 - Geografia")
        print("5 - História")
        print("6 - Educação Física")
        print("7 - Artes")
        print("8 - Algoritmo")
        print("0 - Voltar")

        opcao = input("Escolha a matéria: ")

        if opcao == "1":
            ver_nota("matematica")

        elif opcao == "2":
            ver_nota("portugues")

        elif opcao == "3":
            ver_nota("ciencias")

        elif opcao == "4":
            ver_nota("geografia")

        elif opcao == "5":
            ver_nota("historia")

        elif opcao == "6":
            ver_nota("edf")

        elif opcao == "7":
            ver_nota("artes")

        elif opcao == "8":
            ver_nota("algoritmo")

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")
login()
