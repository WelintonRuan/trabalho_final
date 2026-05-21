CREATE DATABASE IF NOT EXISTS escola;

USE escola;



#TABELA DE USUÁRIOS


CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(50) NOT NULL,
    cargo VARCHAR(10) NOT NULL
);



#TABELA DE PROFESSORES


DROP TABLE IF EXISTS professores;

CREATE TABLE professores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    materia VARCHAR(100),
    login VARCHAR(50)
);


#TABELA DE ALUNOS


CREATE TABLE IF NOT EXISTS alunos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    idade INT,
    turma INT,
    login VARCHAR(50)
);



#TABELA DE NOTAS


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

    media DECIMAL(4,2),
    situacao VARCHAR(20),

    FOREIGN KEY (aluno_id)
    REFERENCES alunos(id)
    ON DELETE CASCADE
);

#LOGIN DO ADM
INSERT INTO usuarios (login, senha, cargo)
VALUES ('admin', '123', 'ADM');


