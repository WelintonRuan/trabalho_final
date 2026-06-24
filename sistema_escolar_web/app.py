from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from database import criar_conexao
from mysql.connector import Error
import bcrypt
import os
from alunos import (
    cadastrar_aluno as cad_aluno,
    listar_alunos,
    remover_aluno as rem_aluno,
    alterar_turma_aluno as alt_turma,
    alterar_nome_aluno as alt_nome_aluno
)
from professor import (
    cadastrar_professor as cad_prof,
    listar_professores,
    remover_professor as rem_prof,
    alterar_materia_professor as alt_materia,
    alterar_nome_professor as alt_nome_prof,
    buscar_materia_professor
)
from notas import lancar_notas, ver_boletim, calcular_media_final

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    if 'usuario' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        
        conn = criar_conexao()
        if not conn:
            flash('Erro ao conectar ao banco de dados', 'danger')
            return render_template('login.html')
        
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT senha, cargo FROM usuarios WHERE login = %s", (usuario,))
            resultado = cursor.fetchone()
            
            if not resultado:
                flash('Usuário ou senha incorretos', 'danger')
                return render_template('login.html')
            
            senha_hash = resultado[0]
            cargo = resultado[1]
            
            if bcrypt.checkpw(senha.encode(), senha_hash.encode()):
                session['usuario'] = usuario
                session['cargo'] = cargo
                flash(f'Bem-vindo, {usuario}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Usuário ou senha incorretos', 'danger')
                
        except Error as e:
            flash(f'Erro: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    cargo = session['cargo']
    if cargo == 'ADM':
        return render_template('dashboard_adm.html')
    elif cargo == 'PROF':
        return render_template('dashboard_prof.html')
    elif cargo == 'ALUNO':
        return render_template('dashboard_aluno.html')
    
    return redirect(url_for('login'))

@app.route('/alunos')
def alunos():
    if 'usuario' not in session or session['cargo'] != 'ADM':
        return redirect(url_for('login'))
    
    conn = criar_conexao()
    alunos_lista = []
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, nome, idade, turma FROM alunos ORDER BY nome")
            alunos_lista = cursor.fetchall()
        except Error as e:
            flash(f'Erro: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()
    
    return render_template('alunos.html', alunos=alunos_lista)

@app.route('/cadastrar_aluno', methods=['POST'])
def cadastrar_aluno():
    if 'usuario' not in session or session['cargo'] != 'ADM':
        return jsonify({'error': 'Não autorizado'}), 401
    
    dados = request.json
    nome = dados.get('nome')
    idade = dados.get('idade')
    turma = dados.get('turma')
    login = dados.get('login')
    senha = dados.get('senha')
    
    if not all([nome, idade, turma, login, senha]):
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400
    
    try:
        idade = int(idade)
        turma = int(turma)
        if idade <= 0 or idade > 100:
            return jsonify({'error': 'Idade inválida'}), 400
    except ValueError:
        return jsonify({'error': 'Idade e turma devem ser números'}), 400
    
    from utils import verificar_login_existente
    if verificar_login_existente(login):
        return jsonify({'error': 'Login já existe'}), 400
    
    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
    
    conn = criar_conexao()
    if not conn:
        return jsonify({'error': 'Erro ao conectar ao banco'}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO alunos (nome, idade, turma, login) VALUES (%s, %s, %s, %s)",
            (nome, idade, turma, login)
        )
        cursor.execute(
            "INSERT INTO usuarios (login, senha, cargo) VALUES (%s, %s, %s)",
            (login, senha_hash, 'ALUNO')
        )
        conn.commit()
        return jsonify({'success': 'Aluno cadastrado com sucesso!'})
    
    except Error as e:
        conn.rollback()
        return jsonify({'error': f'Erro: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/remover_aluno/<int:id>', methods=['DELETE'])
def remover_aluno(id):
    if 'usuario' not in session or session['cargo'] != 'ADM':
        return jsonify({'error': 'Não autorizado'}), 401
    
    conn = criar_conexao()
    if not conn:
        return jsonify({'error': 'Erro ao conectar'}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT login FROM alunos WHERE id = %s", (id,))
        aluno = cursor.fetchone()
        if not aluno:
            return jsonify({'error': 'Aluno não encontrado'}), 404
        
        login_aluno = aluno[0]
        
        cursor.execute("DELETE FROM notas WHERE aluno_id = %s", (id,))
        cursor.execute("DELETE FROM medias_finais WHERE aluno_id = %s", (id,))
        cursor.execute("DELETE FROM alunos WHERE id = %s", (id,))
        cursor.execute("DELETE FROM usuarios WHERE login = %s", (login_aluno,))
        
        conn.commit()
        return jsonify({'success': 'Aluno removido com sucesso!'})
    
    except Error as e:
        conn.rollback()
        return jsonify({'error': f'Erro: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/alterar_aluno', methods=['PUT'])
def alterar_aluno():
    if 'usuario' not in session or session['cargo'] != 'ADM':
        return jsonify({'error': 'Não autorizado'}), 401
    
    dados = request.json
    aluno_id = dados.get('id')
    campo = dados.get('campo')
    valor = dados.get('valor')
    
    if not all([aluno_id, campo, valor]):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    conn = criar_conexao()
    if not conn:
        return jsonify({'error': 'Erro ao conectar'}), 500
    
    cursor = conn.cursor()
    try:
        if campo == 'nome':
            cursor.execute("UPDATE alunos SET nome = %s WHERE id = %s", (valor, aluno_id))
        elif campo == 'turma':
            try:
                valor = int(valor)
                cursor.execute("UPDATE alunos SET turma = %s WHERE id = %s", (valor, aluno_id))
            except ValueError:
                return jsonify({'error': 'Turma deve ser número'}), 400
        else:
            return jsonify({'error': 'Campo inválido'}), 400
        
        conn.commit()
        return jsonify({'success': 'Dados atualizados com sucesso!'})
    
    except Error as e:
        conn.rollback()
        return jsonify({'error': f'Erro: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/professores')
def professores():
    if 'usuario' not in session or session['cargo'] != 'ADM':
        return redirect(url_for('login'))
    
    conn = criar_conexao()
    prof_lista = []
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, nome, materia FROM professores ORDER BY nome")
            prof_lista = cursor.fetchall()
        except Error as e:
            flash(f'Erro: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()
    
    return render_template('professores.html', professores=prof_lista)

@app.route('/cadastrar_professor', methods=['POST'])
def cadastrar_professor():
    if 'usuario' not in session or session['cargo'] != 'ADM':
        return jsonify({'error': 'Não autorizado'}), 401
    
    dados = request.json
    nome = dados.get('nome')
    materia = dados.get('materia')
    login = dados.get('login')
    senha = dados.get('senha')
    
    materias_validas = ['matematica', 'portugues', 'ciencias', 'geografia', 
                        'historia', 'edf', 'artes', 'algoritmo']
    
    if not all([nome, materia, login, senha]):
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400
    
    if materia.lower() not in materias_validas:
        return jsonify({'error': 'Matéria inválida'}), 400
    
    from utils import verificar_login_existente
    if verificar_login_existente(login):
        return jsonify({'error': 'Login já existe'}), 400
    
    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
    
    conn = criar_conexao()
    if not conn:
        return jsonify({'error': 'Erro ao conectar'}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO professores (nome, materia, login) VALUES (%s, %s, %s)",
            (nome, materia.lower(), login)
        )
        cursor.execute(
            "INSERT INTO usuarios (login, senha, cargo) VALUES (%s, %s, %s)",
            (login, senha_hash, 'PROF')
        )
        conn.commit()
        return jsonify({'success': 'Professor cadastrado com sucesso!'})
    
    except Error as e:
        conn.rollback()
        return jsonify({'error': f'Erro: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/remover_professor/<int:id>', methods=['DELETE'])
def remover_professor(id):
    if 'usuario' not in session or session['cargo'] != 'ADM':
        return jsonify({'error': 'Não autorizado'}), 401
    
    conn = criar_conexao()
    if not conn:
        return jsonify({'error': 'Erro ao conectar'}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT login FROM professores WHERE id = %s", (id,))
        prof = cursor.fetchone()
        if not prof:
            return jsonify({'error': 'Professor não encontrado'}), 404
        
        login_prof = prof[0]
        
        cursor.execute("DELETE FROM professores WHERE id = %s", (id,))
        cursor.execute("DELETE FROM usuarios WHERE login = %s", (login_prof,))
        
        conn.commit()
        return jsonify({'success': 'Professor removido com sucesso!'})
    
    except Error as e:
        conn.rollback()
        return jsonify({'error': f'Erro: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/alterar_professor', methods=['PUT'])
def alterar_professor():
    if 'usuario' not in session or session['cargo'] != 'ADM':
        return jsonify({'error': 'Não autorizado'}), 401
    
    dados = request.json
    prof_id = dados.get('id')
    campo = dados.get('campo')
    valor = dados.get('valor')
    
    if not all([prof_id, campo, valor]):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    conn = criar_conexao()
    if not conn:
        return jsonify({'error': 'Erro ao conectar'}), 500
    
    cursor = conn.cursor()
    try:
        if campo == 'nome':
            cursor.execute("UPDATE professores SET nome = %s WHERE id = %s", (valor, prof_id))
        elif campo == 'materia':
            materias_validas = ['matematica', 'portugues', 'ciencias', 'geografia', 
                               'historia', 'edf', 'artes', 'algoritmo']
            if valor.lower() not in materias_validas:
                return jsonify({'error': 'Matéria inválida'}), 400
            cursor.execute("UPDATE professores SET materia = %s WHERE id = %s", (valor.lower(), prof_id))
        else:
            return jsonify({'error': 'Campo inválido'}), 400
        
        conn.commit()
        return jsonify({'success': 'Dados atualizados com sucesso!'})
    
    except Error as e:
        conn.rollback()
        return jsonify({'error': f'Erro: {e}'}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/notas')
def notas():
    if 'usuario' not in session or session['cargo'] != 'PROF':
        return redirect(url_for('login'))
    
    materia = buscar_materia_professor(session['usuario'])
    
    conn = criar_conexao()
    alunos_lista = []
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, nome, turma FROM alunos ORDER BY nome")
            alunos_lista = cursor.fetchall()
        except Error as e:
            flash(f'Erro: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()
    
    return render_template('notas.html', materia=materia, alunos=alunos_lista)

@app.route('/lancar_notas', methods=['POST'])
def lancar_notas_route():
    if 'usuario' not in session or session['cargo'] != 'PROF':
        return jsonify({'error': 'Não autorizado'}), 401
    
    dados = request.json
    aluno_id = dados.get('aluno_id')
    trimestre = dados.get('trimestre')
    nota1 = dados.get('nota1')
    nota2 = dados.get('nota2')
    nota3 = dados.get('nota3')
    
    if not all([aluno_id, trimestre, nota1, nota2, nota3]):
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400
    
    try:
        trimestre = int(trimestre)
        nota1 = float(nota1)
        nota2 = float(nota2)
        nota3 = float(nota3)
        
        if trimestre not in [1, 2, 3]:
            return jsonify({'error': 'Trimestre inválido'}), 400
        
        for nota in [nota1, nota2, nota3]:
            if nota < 0 or nota > 10:
                return jsonify({'error': 'Notas devem estar entre 0 e 10'}), 400
    
    except ValueError:
        return jsonify({'error': 'Valores inválidos'}), 400
    
    materia = buscar_materia_professor(session['usuario'])
    if not materia:
        return jsonify({'error': 'Matéria não encontrada'}), 404
    
    media = round((nota1 + nota2 + nota3) / 3, 2)
    
    conn = criar_conexao()
    if not conn:
        return jsonify({'error': 'Erro ao conectar'}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO notas (aluno_id, materia, trimestre, nota1, nota2, nota3, media_trimestre)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                nota1 = VALUES(nota1),
                nota2 = VALUES(nota2),
                nota3 = VALUES(nota3),
                media_trimestre = VALUES(media_trimestre)
            """,
            (aluno_id, materia, trimestre, nota1, nota2, nota3, media)
        )
        conn.commit()
        
        calcular_media_final(aluno_id, materia)
        
        return jsonify({'success': f'Notas lançadas! Média do {trimestre}º trimestre: {media}'})
    
    except Error as e:
        conn.rollback()
        return jsonify({'error': f'Erro: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/boletim')
def boletim():
    if 'usuario' not in session or session['cargo'] != 'ALUNO':
        return redirect(url_for('login'))
    
    conn = criar_conexao()
    if not conn:
        flash('Erro ao conectar', 'danger')
        return redirect(url_for('dashboard'))
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, nome, turma FROM alunos WHERE login = %s", (session['usuario'],))
        aluno = cursor.fetchone()
        if not aluno:
            flash('Aluno não encontrado', 'danger')
            return redirect(url_for('dashboard'))
        
        aluno_id = aluno[0]
        nome = aluno[1]
        turma = aluno[2]
        
        cursor.execute("SELECT DISTINCT materia FROM notas WHERE aluno_id = %s", (aluno_id,))
        materias = cursor.fetchall()
        
        boletim = {}
        for materia in materias:
            materia_nome = materia[0]
            
            cursor.execute(
                """
                SELECT trimestre, nota1, nota2, nota3, media_trimestre
                FROM notas
                WHERE aluno_id = %s AND materia = %s
                ORDER BY trimestre
                """,
                (aluno_id, materia_nome)
            )
            trimestres = cursor.fetchall()
            
            cursor.execute(
                """
                SELECT media_final, situacao
                FROM medias_finais
                WHERE aluno_id = %s AND materia = %s
                """,
                (aluno_id, materia_nome)
            )
            final = cursor.fetchone()
            
            boletim[materia_nome] = {
                'trimestres': trimestres,
                'media_final': final[0] if final else None,
                'situacao': final[1] if final else None
            }
        
        return render_template('boletim.html', nome=nome, turma=turma, boletim=boletim)
    
    except Error as e:
        flash(f'Erro: {e}', 'danger')
        return redirect(url_for('dashboard'))
    finally:
        cursor.close()
        conn.close()

@app.route('/teste')
def teste():
    return "<h1 style='color:blue; font-size:50px;'>FUNCIONOU!</h1><p>Se você está vendo isso, o Flask está OK.</p>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)