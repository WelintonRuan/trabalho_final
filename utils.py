from binascii import Error


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