-- Tabela Departamento
CREATE TABLE IF NOT EXISTS departamento (
    id_dept SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    id_chefe INT
);

-- Tabela Professor
CREATE TABLE IF NOT EXISTS professor (
    id_prof SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    id_dept INT NOT NULL
);

-- Adiciona a chave estrangeira para o chefe do departamento
ALTER TABLE departamento 
    ADD CONSTRAINT fk_dept_chefe
        FOREIGN KEY(id_chefe)
            REFERENCES professor(id_prof);

-- Tabela Curso
CREATE TABLE IF NOT EXISTS curso (
    id_curso SERIAL PRIMARY KEY,
    curso VARCHAR(100) NOT NULL
);

-- Tabela Disciplina
CREATE TABLE IF NOT EXISTS disciplina (
    cod_disc VARCHAR(6) PRIMARY KEY,
    nome VARCHAR(100),
    id_dept INT
);

-- Tabela Matriz Curricular
CREATE TABLE IF NOT EXISTS matriz_curr (
    id_curso INT NOT NULL,
    cod_disc VARCHAR(6) NOT NULL
);

-- Tabela Grupo TCC
CREATE TABLE IF NOT EXISTS grupo_tcc (
    id_grupo SERIAL PRIMARY KEY,
    id_orientador INT DEFAULT 0,
    status_aprovacao VARCHAR(10), 
    CONSTRAINT fk_grupo_prof
        FOREIGN KEY(id_orientador)
            REFERENCES professor(id_prof)
            ON DELETE SET DEFAULT 
);

-- Tabela Aluno
CREATE TABLE IF NOT EXISTS aluno (
    id_aluno SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    id_curso INT DEFAULT 0,
    id_grupo INT DEFAULT NULL
);

-- Tabela Turma
CREATE TABLE IF NOT EXISTS turma (
    id_turma SERIAL PRIMARY KEY,
    id_prof INT DEFAULT 0 NOT NULL,
    cod_disc VARCHAR(6) NOT NULL,
    ano INT NOT NULL DEFAULT DATE_PART('year', CURRENT_TIMESTAMP),
    semestre NUMERIC(1,0) NOT NULL DEFAULT ((DATE_PART('month', CURRENT_TIMESTAMP) - 1) / 6 + 1)::INT, -- So brincando um pouco
    limite_faltas INT NOT NULL DEFAULT 0
);

-- Tabela Inscricao
CREATE TABLE IF NOT EXISTS inscricao (
    id_insc SERIAL PRIMARY KEY,
    id_aluno INT DEFAULT 0 NOT NULL,
    id_turma INT DEFAULT 0 NOT NULL,
    faltas INT DEFAULT 0,
    media NUMERIC(2,1)
);
