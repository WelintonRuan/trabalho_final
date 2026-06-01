# Sistema Escolar

## Descrição

O Sistema Escolar é uma aplicação desenvolvida em Python integrada ao banco de dados MySQL para gerenciamento de alunos, professores e notas escolares.

O sistema possui diferentes níveis de acesso (Administrador, Professor e Aluno), permitindo o controle de usuários, lançamento de notas e consulta de boletins.

---

## Tecnologias Utilizadas

- Python 3
- MySQL
- MySQL Connector/Python

---

## Funcionalidades

### Administrador

- Cadastrar professores
- Remover professores
- Listar professores
- Alterar nome dos professores
- Alterar matéria dos professores
- Cadastrar alunos
- Remover alunos
- Listar alunos
- Alterar nome dos alunos
- Alterar turma dos alunos

### Professor

- Listar alunos
- Buscar alunos por nome ou ID
- Selecionar trimestre
- Lançar notas
- Atualizar notas já cadastradas
- Calcular médias trimestrais automaticamente

### Aluno

- Consultar boletim
- Visualizar notas por matéria
- Visualizar notas dos três trimestres
- Visualizar médias trimestrais
- Visualizar média final
- Consultar situação final

---

## Controle de Acesso

O sistema possui autenticação por login e senha.

### Tipos de Usuário

| Cargo | Descrição |
|---------|---------|
| ADM | Administrador |
| PROF | Professor |
| ALUNO | Aluno |

### Permissões

**Administrador**
- Gerencia alunos
- Gerencia professores

**Professor**
- Lança notas
- Consulta alunos

**Aluno**
- Consulta seu boletim

---

## Regras de Negócio

### Cadastro de Usuários

- Cada usuário deve possuir um login único.
- Não é permitido cadastrar logins duplicados.

### Cadastro de Professores

- Deve possuir nome.
- Deve possuir uma matéria válida.
- Recebe login e senha de acesso.

### Cadastro de Alunos

- Deve possuir nome.
- Deve possuir idade válida.
- Deve pertencer a uma turma.
- Recebe login e senha de acesso.

### Lançamento de Notas

- Cada matéria possui 3 trimestres.
- Cada trimestre possui 3 notas.
- As notas devem estar entre 0 e 10.
- O professor só pode lançar notas da sua matéria.

### Média Trimestral

```text
(nota1 + nota2 + nota3) / 3
```

### Média Final

```text
(media_trimestre1 + media_trimestre2 + media_trimestre3) / 3
```

### Situação do Aluno

- Média final ≥ 7 → Aprovado
- Média final < 7 → Reprovado

---

##Estrutura do Banco de Dados

### Usuarios

| Campo | Tipo |
|---------|---------|
| id | INT |
| login | VARCHAR(50) |
| senha | VARCHAR(50) |
| cargo | ENUM |

### Professores

| Campo | Tipo |
|---------|---------|
| id | INT |
| nome | VARCHAR(100) |
| materia | VARCHAR(50) |
| login | VARCHAR(50) |

### Alunos

| Campo | Tipo |
|---------|---------|
| id | INT |
| nome | VARCHAR(100) |
| idade | INT |
| turma | INT |
| login | VARCHAR(50) |

### Notas

| Campo | Tipo |
|---------|---------|
| id | INT |
| aluno_id | INT |
| materia | VARCHAR(30) |
| trimestre | INT |
| nota1 | DECIMAL(4,2) |
| nota2 | DECIMAL(4,2) |
| nota3 | DECIMAL(4,2) |
| media_trimestre | DECIMAL(4,2) |

### Medias_Finais

| Campo | Tipo |
|---------|---------|
| id | INT |
| aluno_id | INT |
| materia | VARCHAR(30) |
| media_final | DECIMAL(4,2) |
| situacao | VARCHAR(20) |

---

##F luxo do Sistema

### Login

1. O usuário informa login e senha.
2. O sistema valida as credenciais.
3. O sistema identifica o cargo.
4. O sistema redireciona para o menu correspondente.

### Administrador

1. Faz login.
2. Escolhe administrar alunos ou professores.
3. Realiza operações de cadastro, alteração, consulta e remoção.

### Professor

1. Faz login.
2. Seleciona lançamento de notas.
3. Escolhe um aluno.
4. Seleciona o trimestre.
5. Informa as notas.
6. O sistema calcula e salva as médias.

### Aluno

1. Faz login.
2. Acessa o boletim.
3. Visualiza notas, médias e situação final.

---

##Usuário Administrador Padrão

```text
Login: admin
Senha: 123
```

---

## Como Executar

### 1. Instalar Dependências

```bash
pip install mysql-connector-python
```

### 2. Criar o Banco de Dados

Execute o script SQL fornecido no projeto.

### 3. Configurar a Conexão

Configure a variável de ambiente:

```bash
DB_PASSWORD=sua_senha
```

ou altere diretamente o arquivo de conexão.

### 4. Executar o Sistema

```bash
python main.py
```

---

##Autores

Projeto acadêmico desenvolvido utilizando Python e MySQL para gerenciamento de alunos, professores, notas e boletins escolares.
