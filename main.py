import random
from faker import Faker

faker = Faker('en_US')

# Função para gerar e-mails.
def criar_email(nome):
    nome_parts = nome.lower().split()
    email = f"{nome_parts[0][0]}{nome_parts[1]}@example.edu"
    return email

# Função para gerar departamentos e suas inserções SQL
def criar_departamentos():
    lista_departamentos = [
        ('Computer Science', None),
        ('Engineering', None),
        ('Mathematics', None),
        ('Business Administration', None)
    ]
    insercoes = []
    for depto in lista_departamentos:
        head_id = 'NULL' if depto[1] is None else f"{depto[1]}"
        insercoes.append(
            f"INSERT INTO departamento (nome, id_chefe) VALUES ('{depto[0]}', {head_id});"
        )
    return insercoes, lista_departamentos

# Função para gerar professores e suas inserções SQL
def criar_professores():
    departamentos = [1, 2, 3, 4]
    lista_professores = []
    for i in range(1, 26):
        nome = faker.name()
        email = criar_email(nome)
        depto = random.choice(departamentos)
        lista_professores.append((nome, email, depto))
    
    insercoes = []
    for prof in lista_professores:
        insercoes.append(
            f"INSERT INTO professor (nome, email, id_dept) VALUES ('{prof[0]}', '{prof[1]}', {prof[2]});"
        )
    return insercoes, lista_professores

# Função para gerar cursos e suas inserções SQL
def criar_cursos():
    lista_cursos = [
        ('Computer Science'),
        ('Mechanical Engineering'),
        ('Industrial Engineering'),
        ('Business Analysis'),
    ]
    insercoes = []
    for curso in lista_cursos:
        insercoes.append(
            f"INSERT INTO curso (curso) VALUES ('{curso}');"
        )
    return insercoes, lista_cursos

# Função para gerar disciplinas e suas inserções SQL
def criar_disciplinas():
    lista_disciplinas = [
        ('CS101', 'Introduction to Computer Science', 1),
        ('ME101', 'Introduction to Mechanical Engineering', 2),
        ('IE101', 'Introduction to Industrial Engineering', 2),
        ('BA101', 'Introduction to Business Analysis', 4),
    ]
    insercoes = []
    for disc in lista_disciplinas:
        insercoes.append(
            f"INSERT INTO disciplina (cod_disc, nome, id_dept) VALUES ('{disc[0]}', '{disc[1]}', {disc[2]});"
        )
    return insercoes, lista_disciplinas

# Função para gerar matriz curricular e suas inserções SQL
def criar_matriz_curricular(cursos, disciplinas):
    insercoes = []
    matriz_curricular = []
    for i, curso in enumerate(cursos, start=1):
        for disc in disciplinas:
            if disc[2] == i:
                matriz_curricular.append((i, disc[0]))
                insercoes.append(
                    f"INSERT INTO matriz_curr (id_curso, cod_disc) VALUES ({i}, '{disc[0]}');"
                )
    return insercoes, matriz_curricular

# Função para gerar grupos de TCC e suas inserções SQL
def criar_grupos_tcc():
    lista_grupos = []
    for i in range(1, 11):
        orientador_id = random.randint(1, 25)
        status_aprovacao = random.choice(['analisando', 'reprovado', 'aprovado'])
        lista_grupos.append((orientador_id, status_aprovacao))
    
    insercoes = []
    for grupo in lista_grupos:
        insercoes.append(
            f"INSERT INTO grupo_tcc (id_orientador, status_aprovacao) VALUES ({grupo[0]}, '{grupo[1]}');"
        )
    return insercoes, lista_grupos

# Função para gerar estudantes e suas inserções SQL
def criar_estudantes():
    lista_estudantes = []
    for i in range(1, 101):
        nome = faker.name()
        email = criar_email(nome)
        curso = random.randint(1, 4)
        grupo = random.choice([None] + [i for i in range(1, 11)])
        lista_estudantes.append((i, nome, email, curso, grupo))
    
    insercoes = []
    for est in lista_estudantes:
        grupo_id = 'NULL' if est[4] is None else f"{est[4]}"
        insercoes.append(
            f"INSERT INTO aluno (nome, email, id_curso, id_grupo) VALUES ('{est[1]}', '{est[2]}', {est[3]}, {grupo_id});"
        )
    return insercoes, lista_estudantes

# Função para gerar turmas e suas inserções SQL
def criar_turmas(disciplinas):
    lista_turmas = []
    for disc in disciplinas:
        for _ in range(random.randint(1, 3)):
            professor_id = random.randint(1, 25)
            ano = random.randint(2021, 2024)
            semestre = random.randint(1, 2)
            limite_faltas = random.randint(3, 6)
            lista_turmas.append((professor_id, disc[0], ano, semestre, limite_faltas))
    
    insercoes = []
    for turma in lista_turmas:
        insercoes.append(
            f"INSERT INTO turma (id_prof, cod_disc, ano, semestre, limite_faltas) VALUES ({turma[0]}, '{turma[1]}', {turma[2]}, {turma[3]}, {turma[4]});"
        )
    return insercoes, lista_turmas

# Função para gerar inscrições de alunos em turmas e suas inserções SQL
def criar_inscricoes(estudantes, turmas):
    insercoes = []
    for est in estudantes:
        turmas_por_estudante = random.sample(turmas, k=random.randint(1, len(turmas)//4))
        for turma in turmas_por_estudante:
            faltas = random.randint(0, turma[4])
            media = round(random.uniform(0, 9.9), 1)
            insercoes.append(
                f"INSERT INTO inscricao (id_aluno, id_turma, faltas, media) VALUES ({est[0]}, {turma[0]}, {faltas}, {media});"
            )
    return insercoes

# Função principal para gerar todos os dados e salvar em um arquivo SQL
def gerar_dados():
    with open('inserts.sql', 'w', encoding='utf-8') as arquivo:
        arquivo.write('-- Departmento\n')
        insercoes_departamentos, lista_departamentos = criar_departamentos()
        for insercao in insercoes_departamentos:
            arquivo.write(insercao + '\n')

        arquivo.write('-- Professor\n')
        insercoes_professores, lista_professores = criar_professores()
        for insercao in insercoes_professores:
            arquivo.write(insercao + '\n')

        arquivo.write('-- Curso\n')
        insercoes_cursos, lista_cursos = criar_cursos()
        for insercao in insercoes_cursos:
            arquivo.write(insercao + '\n')

        arquivo.write('-- Disciplina\n')
        insercoes_disciplinas, lista_disciplinas = criar_disciplinas()
        for insercao in insercoes_disciplinas:
            arquivo.write(insercao + '\n')

        arquivo.write('-- Matriz Curricular\n')
        insercoes_matriz, matriz_curricular = criar_matriz_curricular(lista_cursos, lista_disciplinas)
        for insercao in insercoes_matriz:
            arquivo.write(insercao + '\n')

        arquivo.write('-- Grupo TCC\n')
        insercoes_grupos_tcc, lista_grupos_tcc = criar_grupos_tcc()
        for insercao in insercoes_grupos_tcc:
            arquivo.write(insercao + '\n')

        arquivo.write('-- Estudante\n')
        insercoes_estudantes, lista_estudantes = criar_estudantes()
        for insercao in insercoes_estudantes:
            arquivo.write(insercao + '\n')

        arquivo.write('-- Turma\n')
        insercoes_turmas, lista_turmas = criar_turmas(lista_disciplinas)
        for insercao in insercoes_turmas:
            arquivo.write(insercao + '\n')

        arquivo.write('-- Inscricoes\n')
        insercoes_inscricoes = criar_inscricoes(lista_estudantes, lista_turmas)
        for insercao in insercoes_inscricoes:
            arquivo.write(insercao + '\n')

if __name__ == "__main__":
    gerar_dados()
    print("Dados gerados e salvos em 'inserts.sql'")
