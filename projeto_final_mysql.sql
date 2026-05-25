CREATE DATABASE IF NOT EXISTS escola;
USE escola;

-- =====================================
-- TABELA DE USUÁRIOS
-- =====================================

DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(50) NOT NULL,
    cargo ENUM('ADM', 'PROF', 'ALUNO') NOT NULL
);

-- =====================================
-- TABELA DE PROFESSORES
-- =====================================

DROP TABLE IF EXISTS professores;

CREATE TABLE professores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    materia VARCHAR(50) NOT NULL,
    login VARCHAR(50) UNIQUE NOT NULL
);

-- =====================================
-- TABELA DE ALUNOS
-- =====================================

DROP TABLE IF EXISTS alunos;

CREATE TABLE alunos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    idade INT NOT NULL,
    turma INT NOT NULL,
    login VARCHAR(50) UNIQUE NOT NULL
);

-- =====================================
-- TABELA DE NOTAS
-- =====================================

DROP TABLE IF EXISTS notas;

CREATE TABLE notas (

    id INT AUTO_INCREMENT PRIMARY KEY,

    aluno_id INT NOT NULL UNIQUE,

    matematica DECIMAL(4,2) DEFAULT 0,
    portugues DECIMAL(4,2) DEFAULT 0,
    ciencias DECIMAL(4,2) DEFAULT 0,
    geografia DECIMAL(4,2) DEFAULT 0,
    historia DECIMAL(4,2) DEFAULT 0,
    edf DECIMAL(4,2) DEFAULT 0,
    artes DECIMAL(4,2) DEFAULT 0,
    algoritmo DECIMAL(4,2) DEFAULT 0,

    media DECIMAL(4,2) DEFAULT 0,
    situacao VARCHAR(20) DEFAULT 'Reprovado',

    CONSTRAINT fk_notas_aluno
        FOREIGN KEY (aluno_id)
        REFERENCES alunos(id)
        ON DELETE CASCADE
);

-- =====================================
-- ADMINISTRADOR PADRÃO
-- =====================================

INSERT IGNORE INTO usuarios (login, senha, cargo)
VALUES ('admin', '123', 'ADM');