-- As queries foram feitas de modo que seja possivel retirar a parte com variavel para retornar a lista completa de cada item

-- 1) Histórico escolar dos alunos
SELECT
    aluno.nome AS nome_aluno,
    disciplina.cod_disc,
    disciplina.nome AS nome_disc,
    turma.ano,
    turma.semestre,
    inscricao.media,
    inscricao.faltas
FROM aluno
INNER JOIN inscricao ON aluno.id_aluno = inscricao.id_aluno
INNER JOIN turma ON turma.id_turma = inscricao.id_turma
INNER JOIN disciplina ON turma.cod_disc = disciplina.cod_disc
WHERE
    1 = 1
    AND aluno.id_aluno = $1 -- Comentar aqui caso queira todo mundo
ORDER BY
    aluno.id_aluno,
    turma.ano,
    turma.semestre -- Para caso for ver todos
;

-- 2) Histórico de disciplinas ministradas pelos professores
SELECT
    professor.nome,
    disciplina.cod_disc,
    disciplina.nome AS nome_disc,
    turma.ano,
    turma.semestre
FROM professor
INNER JOIN turma ON professor.id_prof = turma.id_prof
INNER JOIN disciplina ON turma.cod_disc = disciplina.cod_disc
WHERE
    1 = 1
    AND professor.id_prof = $1 -- Comentar aqui caso queira todo mundo
ORDER BY -- Para caso for ver todos
    professor.id_prof, 
    turma.ano, 
    turma.semestre
;

-- 3) Listar alunos que já se formaram (foram aprovados em todos os cursos de uma matriz curricular) em um determinado semestre de um ano
-- Considerando a falta de ordem obrigatória das materias, a query vai retornar aqueles que se formaram ate ate certo ano
---------------------
-- IMPORTANTE
---------------------
-- Dependendo da sua sorte ou azar na geracao de dados, pode ser possivel que nao tenha ninguem aprovado dado a grande quantidade de requisitos
-- Para resolver isso, pode-se criar dados manualmente que caibam em todos os requisitos ou, alternativamente, pode-se retirar alguns requisitos para aparecer as listas
-- Por exemplo, comentando COUNT(DISTINCT turma.cod_disc) = MAX(n_disciplinas_curso.n_disc) geralmente eh o suficiente para ver algum resultado
WITH n_disciplinas_curso AS (SELECT id_curso, COUNT(*) AS n_disc FROM matriz_curr GROUP BY id_curso)
SELECT
    aluno.id_aluno,
    aluno.nome,
    COUNT(DISTINCT turma.cod_disc) AS n_aprovacoes,
    MAX(turma.ano * 10 + turma.semestre) AS ultima_aprovacao -- Aqui estou pegando o ultimo ano/materia em que o aluno foi aprovado em algo no formato seguindo o exemplo (20242 -> segundo semestre de 2024)
    -- PostgreSQL nao precisa de CAST para concatenar numeros, bem pratico
FROM aluno
INNER JOIN inscricao ON aluno.id_aluno = inscricao.id_aluno
INNER JOIN turma ON inscricao.id_turma = turma.id_turma
INNER JOIN n_disciplinas_curso ON aluno.id_curso = n_disciplinas_curso.id_curso
INNER JOIN grupo_tcc ON aluno.id_grupo = grupo_tcc.id_grupo
WHERE
    inscricao.media >= 5
    AND turma.limite_faltas >= inscricao.faltas
    AND grupo_tcc.status_aprovacao = 'aprovado'
GROUP BY aluno.id_aluno
HAVING
    1 = 1
    AND COUNT(DISTINCT turma.cod_disc) = MAX(n_disciplinas_curso.n_disc) -- Comentar aqui para tentar ver alguma coisa
    AND MAX(turma.ano * 10 + turma.semestre) <= ($1 * 10 + $2) -- Ano, mes
;

-- 4) Chefes de departamento
SELECT
    professor.nome as nome_prof,
    departamento.nome AS nome_dept
FROM professor
INNER JOIN departamento ON professor.id_prof = departamento.id_chefe
;

-- 5) Grupos de TCC
SELECT
    grupo_tcc.id_grupo,
    professor.nome AS nome_professor,
    LEFT(CONCAT_AGG(CONCAT(aluno.nome, ', ')), LENGTH(CONCAT_AGG(CONCAT(aluno.nome, ', '))) - 2) AS nomes_alunos -- A segunda parte eh pra tirar o ultimo ', '
FROM grupo_tcc
INNER JOIN aluno ON grupo_tcc.id_grupo = aluno.id_grupo 
INNER JOIN professor ON grupo_tcc.id_orientador = professor.id_prof
GROUP by
	grupo_tcc.id_grupo,
	professor.nome
ORDER BY grupo_tcc.id_grupo;

-- Para versoes mais recentes do PostgreSQL
SELECT
    grupo_tcc.id_grupo,
    STRING_AGG(aluno.nome, ", ") AS nomes_alunos,
    professor.nome AS nome_professor
FROM grupo_tcc
INNER JOIN aluno ON grupo_tcc.id_grupo = aluno.id_grupo 
INNER JOIN professor ON grupo_tcc.id_orientador = professor.id_prof
GROUP BY grupo_tcc.id_grupo
;
