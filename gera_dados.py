import sqlalchemy as sql
import os
import faker
import random
from unidecode import unidecode

def lista_de_lista_para_insert(lista, tabela, colunas):
    colunas = ", ".join(colunas)
    query = f"INSERT INTO {tabela}({colunas}) VALUES " + ",".join(["("+",".join([f"'{dados}'" if type(dados) == str else f"{dados}" for dados in item]) + ")\n" for item in lista]) + ";"
    query = query.replace("'NULL'", "NULL")
    return query

fk = faker.Faker('pt_BR')

# Numeros para definir quantidade gerada
n_profs = 3 # Numero de profs por departamento
n_disc_per_matr = 5 # Numero de disciplinas por matriz curricular
n_grps = int(len(profs) * 2/3) # Numero total de grupos de tcc
n_alunos = 100 # Numero total de alunos
n_turmas_per_prof = 3 # Numero de turmas por professor

# Departamentos
depts = [
    "Matemática",
    "Física",
    "Ciências Sociais",
    "Ciência da Computação",
    "Administração"
]
insert_depts = f"INSERT INTO departamento(nome, id_chefe) VALUES " + ", ".join([f"('{dept}', NULL)" for dept in depts]) + ";"
insert_depts

# Professores
profs = [[fk.name()] for _ in range(len(depts) * n_profs)]
[profs[i].append(".".join(unidecode(profs[i][0]).split(" ")[:2]).lower() + "@collegedb.com") for i in range(len(profs))]
[profs[i].append(random.randint(1, len(depts))) for i in range(len(profs))]
insert_profs = lista_de_lista_para_insert(profs, "professor", ["nome", "email", "id_dept"])

updates_dept = ""
for i in range(len(depts)):
    profs_dept = [j for j, prof in enumerate(profs) if prof[2] == i + 1]
    if len(profs_dept) == 0:
        continue
    escolhido = random.choice(profs_dept)
    updates_dept += "UPDATE departamento SET id_chefe = " + str(escolhido + 1) + " WHERE id_dept = " + str(i + 1) + ";\n"

# Curso
cursos = [
    "Ciência da Computação",
    "Engenharia Elétrica",
    "Engenharia Mecânica",
    "Engenharia de Produção",
    "Engenharia Têxtil",
    "Administração",
    "Ciência de Dados"
]
insert_cursos = f"INSERT INTO curso(nome) VALUES " + ", ".join([f"('{curso}')" for curso in cursos]) + ";"

# Disciplinas
discs = [[unidecode(dept[:2]).upper() + "1001", n + 1] if len(dept.split(" ")) == 1 else [dept.split(" ")[0][0].upper() + dept.split(" ")[-1][0].upper() + "1001", n + 1] for n, dept in enumerate(depts)]
for i in range(len(discs)):
    discs.append([discs[i][0].replace("1","2"), discs[i][1]])
[discs[i].append("Introdução a " + depts[i % len(depts)]) if i < len(discs)/2 else discs[i].append("Tópicos Avançados de " + depts[i % len(depts)]) for i, disc in enumerate(discs)]
insert_discs = lista_de_lista_para_insert(discs, "disciplina", ["cod_disc", "id_dept", "nome"])

# Matriz Curricular
temp = [[disc[0] for disc in random.sample(discs, n_disc_per_matr)] for _ in range(len(cursos))]
mc = []
for i, cods_discs in enumerate(temp):
    for cod_disc in cods_discs:
        mc.append([i+1, cod_disc])
insert_mc = lista_de_lista_para_insert(mc, "matriz_curr", ["id_curso", "cod_disc"])
insert_mc = insert_mc[:-1]
insert_mc += "ON CONFLICT (id_curso, cod_disc) DO NOTHING;"

# Grupo TCC
grps = [[random.randint(1, len(profs)), random.choice(["analisando", "aprovado", "reprovado"])] for i in range(n_grps)]
insert_grps = lista_de_lista_para_insert(grps, "grupo_tcc", ["id_orientador", "status_aprovacao"])

# Alunos
nomes = [fk.name() for _ in range(n)]
emails = [".".join(unidecode(nomes[i]).split(" ")[:2]).lower() + "@collegedb.com" for i in range(n_alunos)]
id_cursos = [random.randint(1, len(cursos)) for _ in range(n_alunos)]
grps_n_integrantes = [0 for _ in range(n_grps)]
limite_per_grp = 3
id_grupos = []
for i in range(n_alunos):
    if random.choice(["grupo", "NULL"]) == "NULL":
        id_grupos.append("NULL")
        continue
    while(True):
        id_grupo = random.randint(1, n_grps)
        if grps_n_integrantes[id_grupo - 1] < limite_per_grp:
            id_grupos.append(id_grupo)
            break
alunos = [[nomes[i], emails[i], id_cursos[i], id_grupos[i]] for i in range(n_alunos)]
insert_alunos = lista_de_lista_para_insert(alunos, "aluno", ["nome", "email", "id_curso", "id_grupo"])

# Turmas
temp = [random.choices([disc[0] for disc in discs if disc[1] == prof[2]], k = n_turmas_per_prof) for prof in profs]
turmas = []
for i, discs_temp in enumerate(temp):
    for disc in discs_temp:
        turmas.append([disc, i+1, random.randint(2010, 2024), random.randint(1, 2), random.randint(10,20)])
insert_turmas = lista_de_lista_para_insert(turmas, "turma", ["cod_disc", "id_prof", "ano", "semestre", "limite_faltas"])

# Inscricao
inscricoes = []
for i, aluno in enumerate(alunos):
    mc_aluno = [discs_mc[1] for discs_mc in mc[(aluno[2]-1)*n_disc_per_matr:(aluno[2]-1)*n_disc_per_matr+n_disc_per_matr]]
    inscrito = [0 for _ in range(n_disc_per_matr)]
    for j, turma in enumerate(turmas):
        if turma[0] in mc_aluno:
            index = mc_aluno.index(turma[0])
            if inscrito[index] == 0:
                if random.randint(0,10) >= 7: # Aumentar a chance da pessoa nao ter cursado alguma materia ainda
                    inscrito[index] = -1
                    continue
                inscricoes.append([i + 1, j + 1, random.randint(0, 25), round(random.uniform(0, 10), 1)])
                inscrito[index] = 1
insert_inscricoes = lista_de_lista_para_insert(inscricoes, "inscricao", ["id_aluno", "id_turma", "faltas", "media"])

en = sql.create_engine(os.environ['DATABASE_URL'])

# Caso tudo de errado
# Lembrando que esta tudo com encoding 
with open(os.path.join(r"D:\GitHub\CollegeDB", "sql", "inserts.sql"), "w") as f:
    f.write(insert_depts)
    f.write("\n\n")
    
    f.write(insert_profs)
    f.write("\n\n")

    f.write(updates_dept)
    f.write("\n\n")

    f.write(insert_cursos)
    f.write("\n\n")

    f.write(insert_discs)
    f.write("\n\n")

    f.write(insert_mc)
    f.write("\n\n")

    f.write(insert_grps)
    f.write("\n\n")

    f.write(insert_alunos)
    f.write("\n\n")

    f.write(insert_turmas)
    f.write("\n\n")

    f.write(insert_inscricoes)
    f.write("\n\n")

with en.connect() as conn:
    conn.execute(sql.text(insert_depts))
    conn.commit()

    conn.execute(sql.text(insert_profs))
    conn.commit()

    conn.execute(sql.text(updates_dept))
    conn.commit()

    conn.execute(sql.text(insert_cursos))
    conn.commit()

    conn.execute(sql.text(insert_discs))
    conn.commit()

    conn.execute(sql.text(insert_mc))
    conn.commit()

    conn.execute(sql.text(insert_grps))
    conn.commit()

    conn.execute(sql.text(insert_alunos))
    conn.commit()

    conn.execute(sql.text(insert_turmas))
    conn.commit()

    conn.execute(sql.text(insert_inscricoes))
    conn.commit()
