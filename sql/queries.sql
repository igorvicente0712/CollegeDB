--- 1 - histórico escolar de qualquer aluno, retornando o código e nome da disciplina, semestre e ano que a disciplina foi cursada e nota final
SELECT
    aluno.id_aluno,
    aluno.nome AS nome_aluno,
    disciplina.cod_disc,
    disciplina.nome AS nome_disc,
    turma.semestre,
    turma.ano,
    inscricao.media AS nota_final
FROM aluno
INNER JOIN inscricao ON aluno.id_aluno = inscricao.id_aluno
INNER JOIN turma ON turma.id_turma = inscricao.id_turma
INNER JOIN disciplina ON turma.cod_disc = disciplina.cod_disc
ORDER BY aluno.id_aluno, turma.ano, turma.semestre;

--- 2 - histórico de disciplinas ministradas por qualquer professor, com semestre e ano
SELECT
    professor.id_prof,
    professor.nome AS nome_professor,
    disciplina.cod_disc,
    disciplina.nome AS nome_disc,
    turma.semestre,
    turma.ano
FROM professor
INNER JOIN turma ON professor.id_prof = turma.id_prof
INNER JOIN disciplina ON turma.cod_disc = disciplina.cod_disc
ORDER BY professor.id_prof, turma.ano, turma.semestre;

--- 3 - listar alunos que já se formaram (foram aprovados em todos os cursos de uma matriz curricular) em um determinado semestre de um ano
--- Substitua $1 e $2 pelos valores de ano e semestre desejados.
WITH n_disciplinas_curso AS (
    SELECT id_curso, COUNT(*) AS n_disc FROM matriz_curr GROUP BY id_curso
)
SELECT
    aluno.id_aluno,
    aluno.nome,
    COUNT(DISTINCT turma.cod_disc) AS n_aprovacoes,
    MAX(turma.ano * 10 + turma.semestre) AS ultima_aprovacao 
FROM aluno
INNER JOIN inscricao ON aluno.id_aluno = inscricao.id_aluno
INNER JOIN turma ON inscricao.id_turma = turma.id_turma
INNER JOIN n_disciplinas_curso ON aluno.id_curso = n_disciplinas_curso.id_curso
WHERE
    inscricao.media >= 5
    AND turma.limite_faltas >= inscricao.faltas
GROUP BY aluno.id_aluno
HAVING
    COUNT(DISTINCT turma.cod_disc) = MAX(n_disciplinas_curso.n_disc)
    AND MAX(turma.ano * 10 + turma.semestre) <= ($1 * 10 + $2); -- Ano, semestre


--- 4 - listar todos os professores que são chefes de departamento, junto com o nome do departamento
SELECT
    grupo_tcc.id_grupo,
    STRING_AGG(aluno.nome, ', ') AS nomes_alunos,
    professor.nome AS nome_professor
FROM grupo_tcc
INNER JOIN aluno ON grupo_tcc.id_grupo = aluno.id_grupo 
INNER JOIN professor ON grupo_tcc.id_orientador = professor.id_prof
GROUP BY grupo_tcc.id_grupo, professor.nome;


--- 5 -  saber quais alunos formaram um grupo de TCC e qual professor foi o orientador
SELECT
    grupo_tcc.id_grupo,
    STRING_AGG(aluno.nome, ', ') AS nomes_alunos,
    professor.nome AS nome_professor
FROM grupo_tcc
INNER JOIN aluno ON grupo_tcc.id_orientador = aluno.id_grupo 
INNER JOIN professor ON grupo_tcc.id_orientador = professor.id_prof
GROUP BY grupo_tcc.id_grupo, professor.nome;

