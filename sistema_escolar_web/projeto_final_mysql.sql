CREATE DATABASE IF NOT EXISTS escola;
USE escola;



#USUÁRIOS


CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    cargo ENUM('ADM', 'PROF', 'ALUNO') NOT NULL
);


#PROFESSORES

CREATE TABLE IF NOT EXISTS professores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    materia VARCHAR(50) NOT NULL,
    login VARCHAR(50) UNIQUE NOT NULL
);


#ALUNOS


CREATE TABLE IF NOT EXISTS alunos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    idade INT NOT NULL,
    turma INT NOT NULL,
    login VARCHAR(50) UNIQUE NOT NULL
);


#NOTAS POR TRIMESTRE


CREATE TABLE IF NOT EXISTS notas (

    id INT AUTO_INCREMENT PRIMARY KEY,

    aluno_id INT NOT NULL,

    materia VARCHAR(30) NOT NULL,

    trimestre INT NOT NULL,

    nota1 DECIMAL(4,2) NOT NULL,
    nota2 DECIMAL(4,2) NOT NULL,
    nota3 DECIMAL(4,2) NOT NULL,

    media_trimestre DECIMAL(4,2),

    CONSTRAINT  fk_notas_aluno
        FOREIGN KEY (aluno_id)
        REFERENCES alunos(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_aluno_materia_trimestre
        UNIQUE (aluno_id, materia, trimestre)
);


#MÉDIAS FINAIS


CREATE TABLE IF NOT EXISTS medias_finais (

    id INT AUTO_INCREMENT PRIMARY KEY,

    aluno_id INT NOT NULL,

    materia VARCHAR(30) NOT NULL,

    media_final DECIMAL(4,2),

    situacao VARCHAR(20),

    CONSTRAINT fk_media_aluno
        FOREIGN KEY (aluno_id)
        REFERENCES alunos(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_aluno_materia
        UNIQUE (aluno_id, materia)
);


#ADMINISTRADOR PADRÃO


INSERT INTO usuarios (login, senha, cargo)
VALUES ('admin', '*Coloque o hash que você gerou em (gerar_hash.py)', 'ADM');