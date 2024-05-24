-- Caso alguma pessoa, seja professor ou aluno, queira suas informacoes deletadas, optei por colocar seu id como 0, mas podia ser ON DELETE CASCADE tambem

CREATE TABLE IF NOT EXISTS departamento (
    id_dept INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nome VARCHAR(100) NOT NULL,
    id_chefe INT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS professor (
    id_prof INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    id_dept INT NOT NULL,
    CONSTRAINT fk_prof_dept
        FOREIGN KEY(id_dept)
            REFERENCES departamento(id_dept)
);

ALTER TABLE departamento 
    ADD CONSTRAINT fk_dept_chefe
        FOREIGN KEY(id_chefe)
            REFERENCES professor(id_prof);

CREATE TABLE IF NOT EXISTS curso (
    id_curso INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nome VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS disciplina (
    cod_disc VARCHAR(6) PRIMARY KEY,
    nome VARCHAR(100),
    id_dept INT,
    CONSTRAINT fk_disc_dept
        FOREIGN KEY(id_dept)
            REFERENCES departamento(id_dept)
);

CREATE TABLE IF NOT EXISTS matriz_curr (
    id_curso INT NOT NULL,
    cod_disc VARCHAR(6) NOT NULL,
    PRIMARY KEY (id_curso, cod_disc),
    CONSTRAINT fk_mat_curso
        FOREIGN KEY(id_curso)
            REFERENCES curso(id_curso),
    CONSTRAINT fk_mat_disc
        FOREIGN KEY(cod_disc)
            REFERENCES disciplina(cod_disc)
);

CREATE TABLE IF NOT EXISTS grupo_tcc (
    id_grupo INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    id_orientador INT DEFAULT 0,
    status_aprovacao VARCHAR(10), -- analisando, reprovado, aprovado, talvez se fosse usar ENUM fosse melhor?
    CONSTRAINT fk_grupo_prof
        FOREIGN KEY(id_orientador)
            REFERENCES professor(id_prof)
            ON DELETE SET DEFAULT 
);

CREATE TABLE IF NOT EXISTS aluno (
    id_aluno INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    id_curso INT DEFAULT 0,
    id_grupo INT DEFAULT NULL, -- Da pra colocar na tabela de grupo_tcc, mas achei melhor assim
    CONSTRAINT fk_aluno_curso
        FOREIGN KEY(id_curso)
            REFERENCES curso(id_curso)
            ON DELETE SET DEFAULT,
    CONSTRAINT fk_aluno_grupo
        FOREIGN KEY(id_grupo)
            REFERENCES grupo_tcc(id_grupo)
            ON DELETE SET DEFAULT
);

-- Turmas com sua respectiva disciplina e professor que leciona, assim como ano e semestre
CREATE TABLE IF NOT EXISTS turma (
    id_turma INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    id_prof INT DEFAULT 0 NOT NULL,
    cod_disc VARCHAR(6) NOT NULL DEFAULT '0',
    ano INT NOT NULL DEFAULT DATE_PART('year', CURRENT_TIMESTAMP),
    semestre NUMERIC(1,0) NOT NULL DEFAULT (DIV(DATE_PART('month', CURRENT_TIMESTAMP) - 1, 6) + 1), -- So brincando um pouco
    limite_faltas INT NOT NULL DEFAULT 0,
    CONSTRAINT fk_turma_prof
        FOREIGN KEY(id_prof)
            REFERENCES professor(id_prof)
            ON DELETE SET DEFAULT,
    CONSTRAINT fk_turma_disc
        FOREIGN KEY(cod_disc)
            REFERENCES disciplina(cod_disc)
            ON DELETE SET DEFAULT
);

-- Inscricao individual dos alunos nas suas turmas de escolha
CREATE TABLE IF NOT EXISTS inscricao (
    id_insc INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    id_aluno INT DEFAULT 0 NOT NULL,
    id_turma INT DEFAULT 0 NOT NULL,
    faltas INT DEFAULT 0,
    media NUMERIC(3,1),
    CONSTRAINT fk_insc_aluno
        FOREIGN KEY(id_aluno)
            REFERENCES aluno(id_aluno)
            ON DELETE SET DEFAULT,
    CONSTRAINT fk_insc_turma
        FOREIGN KEY(id_turma)
            REFERENCES turma(id_turma)
            ON DELETE SET DEFAULT
);