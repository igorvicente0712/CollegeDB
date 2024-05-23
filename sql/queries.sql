-- As queries foram feitas de modo que, para fazer a busca, eh necessario mudar a parte com "?".
-- Feito dessa maneira pois alguns softwares entendem a interrogacao como uma variavel a ser mudada (e.g. Excel)
-- Foram feitas tambem de modo que seja possivel retirar a parte com "?" para retornar a lista completa de cada item

-- 1) Histórico escolar dos alunos
SELECT
    aluno.nome AS nome_aluno,
    disciplina.id_disc,
    disciplina.nome AS nome_disc,
    turma.semestre,
    turma.ano,
    inscricao.media
FROM aluno
INNER JOIN inscricao ON aluno.id_aluno = inscricao.id_aluno
INNER JOIN turma ON turma.id_turma = inscricao.id_turma
INNER JOIN disciplina ON turma.id_disc = disciplina.id_disc
WHERE
    1 = 1
    AND id_aluno = ? -- Comentar aqui caso queira todo mundo
ORDER BY aluno.id_aluno -- Para caso for ver todos
;

-- 2) Histórico de disciplinas ministradas pelos professores
SELECT
    professor.nome,
    disciplina.id_disc,
    disciplina.nome AS nome_disc,
    turma.semestre,
    turma.ano
FROM professor
INNER JOIN turma ON professor.id_prof = turma.id_prof
INNER JOIN disciplina ON turma.id_disc = disciplina.id_disc
WHERE
    1 = 1
    AND id_prof = ? -- Comentar aqui caso queira todo mundo
ORDER BY -- Para caso for ver todos
    professor.id_prof, 
    turma.ano, 
    turma.semestre

-- 3) Listar alunos que já se formaram (foram aprovados em todos os cursos de uma matriz curricular) em um determinado semestre de um ano
-- Considerando a falta de ordem obrigatória das materias, a query vai retornar aqueles que se formaram ate ate certo ano
WITH n_disciplinas_curso AS (SELECT id_curso, COUNT(*) AS n_disc FROM matriz_curr)
SELECT
    aluno.id_aluno,
    aluno.nome,
    COUNT(DISTINCT turma.id_disc) AS n_aprovacoes,
    MAX(CONCAT(turma.ano + turma.semestre)) AS ultima_aprovacao -- Aqui estou pegando o ultimo ano/materia em que o aluno foi aprovado em algo no formato seguindo o exemplo (202402 -> segundo semestre de 2024)
    -- PostgreSQL nao precisa de CAST para concatenar numeros, bem pratico
FROM aluno
INNER JOIN inscricao ON aluno.id_aluno = inscricao.id_aluno
INNER JOIN turma ON inscricao.id_turma = turma.id_turma
INNER JOIN n_disciplinas_curso ON aluno.id_curso = n_disciplinas_curso.id_curso
WHERE
    inscricao.media >= 5
    AND turma.limite_falta >= inscricao.faltas
GROUP BY aluno.id_aluno
HAVING
    n_aprovacoes = MAX(n_disciplinas_curso.n_disc)
    AND ultima_aprovacao <= CONCAT(?,?) -- Ano, mes


-- 4) Chefes de departamento
SELECT
    professor.nome as nome_prof,
    departamento.nome AS nome_dept
FROM professor
INNER JOIN departamento ON professor.id_prof = departamento.id_chefe

-- 5) Grupos de TCC
SELECT
    grupo_tcc.id_grupo,
    STRING_AGG(aluno.nome, ", ") AS nomes_alunos,
    professor.nome AS nome_professor
FROM grupo_tcc
INNER JOIN aluno ON grupo_tcc.id_grupo = aluno.id_grupo 
INNER JOIN professor ON grupo_tcc.id_prof = professor.id_prof
GROUP BY grupo_tcc.id_grupo