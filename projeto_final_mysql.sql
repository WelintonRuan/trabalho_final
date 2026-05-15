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


CREATE TABLE IF NOT EXISTS professores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    materia VARCHAR(100)
);


#TABELA DE ALUNOS


CREATE TABLE IF NOT EXISTS alunos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    idade INT,
    turma INT
);



#TABELA DE NOTAS


CREATE TABLE IF NOT EXISTS notas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aluno_id INT NOT NULL,
    nota_1trimestre DECIMAL(4,2),
    nota_2trimestre DECIMAL(4,2),
    nota_3trimestre DECIMAL(4,2),
    media DECIMAL(4,2),
    situacao VARCHAR(50),
    FOREIGN KEY (aluno_id)
    REFERENCES alunos(id)
        ON DELETE CASCADE
);


#LOGIN DO ADM
INSERT INTO usuarios (login, senha, cargo)
VALUES ('admin', '123', 'ADM');



