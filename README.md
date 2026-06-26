# 🎓 Sistema Escolar Web

Sistema desenvolvido em **Python + Flask + MySQL** para gerenciamento escolar.

Permite controle de acesso por perfil (**Administrador, Professor e Aluno**), gerenciamento de usuários, lançamento de notas e consulta de boletins.

---

# 📌 Funcionalidades

## 👨‍💼 Administrador

* Cadastrar professores
* Remover professores
* Listar professores
* Alterar nome dos professores
* Alterar matéria dos professores
* Cadastrar alunos
* Remover alunos
* Listar alunos
* Alterar nome dos alunos
* Alterar turma dos alunos

---

## 👨‍🏫 Professor

* Listar alunos
* Buscar alunos por nome ou ID
* Selecionar trimestre
* Lançar notas
* Atualizar notas já cadastradas

---

## 👨‍🎓 Aluno

* Consultar boletim
* Visualizar notas por matéria
* Visualizar médias trimestrais
* Visualizar média final
* Consultar situação final

---

# 🛠 Tecnologias Utilizadas

## Backend

* Python 3
* Flask
* MySQL
* mysql-connector-python
* bcrypt

## Frontend

* HTML5
* CSS3

---

# 🔐 Controle de Acesso

| Cargo | Permissão                      |
| ----- | ------------------------------ |
| ADM   | Gerenciar alunos e professores |
| PROF  | Lançar notas                   |
| ALUNO | Consultar boletim              |

---

# 📚 Regras de Negócio

## Usuários

* Login único
* Não permite duplicidade
* Senhas armazenadas com Hash (bcrypt)

## Professores

* Nome obrigatório
* Matéria válida
* Login e senha obrigatórios

## Alunos

* Nome obrigatório
* Idade válida
* Turma obrigatória
* Login e senha obrigatórios

## Notas

* 3 trimestres por matéria
* 3 notas por trimestre
* Notas entre **0 e 10**
* Professor lança apenas notas da própria matéria

---

# 📐 Fórmulas

## Média Trimestral

```text
(nota1 + nota2 + nota3) / 3
```

## Média Final

```text
(media1 + media2 + media3) / 3
```

## Situação Final

```text
≥ 7 → Aprovado
< 7 → Reprovado
```

---

# 🗄 Banco de Dados

## usuarios

| Campo | Tipo         |
| ----- | ------------ |
| id    | INT          |
| login | VARCHAR(50)  |
| senha | VARCHAR(255) |
| cargo | ENUM         |

## professores

| Campo   | Tipo         |
| ------- | ------------ |
| id      | INT          |
| nome    | VARCHAR(100) |
| materia | VARCHAR(50)  |
| login   | VARCHAR(50)  |

## alunos

| Campo | Tipo         |
| ----- | ------------ |
| id    | INT          |
| nome  | VARCHAR(100) |
| idade | INT          |
| turma | INT          |
| login | VARCHAR(50)  |

## notas

| Campo           | Tipo         |
| --------------- | ------------ |
| id              | INT          |
| aluno_id        | INT          |
| materia         | VARCHAR(30)  |
| trimestre       | INT          |
| nota1           | DECIMAL(4,2) |
| nota2           | DECIMAL(4,2) |
| nota3           | DECIMAL(4,2) |
| media_trimestre | DECIMAL(4,2) |

## medias_finais

| Campo       | Tipo         |
| ----------- | ------------ |
| id          | INT          |
| aluno_id    | INT          |
| materia     | VARCHAR(30)  |
| media_final | DECIMAL(4,2) |
| situacao    | VARCHAR(20)  |

---

# 🔄 Fluxo do Sistema

```text
Login
 ↓
Validação
 ↓

ADM
├── Gerenciar Alunos
└── Gerenciar Professores

PROF
└── Lançar Notas

ALUNO
└── Consultar Boletim
```

---

# 📁 Estrutura do Projeto

```text
projeto/

app.py
database.py

templates/
├── login.html
├── adm.html
├── professor.html
└── aluno.html

static/
├── css/
└── img/

alunos.py
professor.py
notas.py
utils.py
```

---

# 👤 Usuário Administrador Padrão

```text
Login: admin
Senha: admin123
```

---

# 🚀 Como Executar

## Instalar Dependências

```bash
pip install flask
pip install mysql-connector-python
pip install bcrypt
```

## Configurar Banco

Execute o script SQL do projeto.

## Configurar Variável de Ambiente

```bash
DB_PASSWORD=sua_senha
```

## Executar

```bash
python app.py
```

Acesse:

```text
http://127.0.0.1:5000
```

---

# 👥 Autores

Projeto acadêmico desenvolvido utilizando:

* Flask
* Python
* HTML
* CSS
* MySQL
