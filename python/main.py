from faker import Faker
import random
import unicodedata

fake = Faker('en_US')

def remove_accents(text):
    nfkd = unicodedata.normalize('NFKD', text)
    return u"".join([c for c in nfkd if not unicodedata.combining(c)])

def generate_email(name):
    name_without_accents = remove_accents(name).lower().split()
    email = f"{name_without_accents[0][0]}{name_without_accents[1]}@example.edu"
    return email

def generate_department():
    departments = [
        ('Computer Science', 100000, 'Building A', None),
        ('Engineering', 100000, 'Building B', None),
        ('Mathematics', 100000, 'Building C', None),
        ('Business Administration', 100000, 'Building D', None)
    ]
    inserts = []
    for dept in departments:
        head_id = 'NULL' if dept[3] is None else f"'{dept[3]}'"
        inserts.append(f"INSERT INTO Department (department_name, Budget, Building, head_id) VALUES ('{dept[0]}', {dept[1]}, '{dept[2]}', {head_id});")
    return inserts, departments

def generate_professor():
    departments = ['Computer Science', 'Engineering', 'Mathematics', 'Business Administration']
    professors = []
    for i in range(1, 26):
        id = f'P{i:03d}'
        ssn = fake.ssn()
        name = fake.name()
        email = generate_email(name)
        salary = random.randint(4000, 15000)
        dept = random.choice(departments)
        professors.append((id, ssn, name, email, salary, dept))
    inserts = []
    for prof in professors:
        inserts.append(f"INSERT INTO Professor (ID, SSN, Name, Email, Salary, department_name) VALUES ('{prof[0]}', '{prof[1]}', '{remove_accents(prof[2])}', '{prof[3]}', {prof[4]}, '{prof[5]}');")
    return inserts, professors

def generate_course():
    courses = [
        ('CS101', 'Computer Science', 'Computer Science'),
        ('ME101', 'Mechanical Engineering', 'Engineering'),
        ('IE101', 'Industrial Engineering', 'Engineering'),
        ('BA101', 'Business Administration', 'Business Administration'),
        ('MA101', 'Mathematics', 'Mathematics'),
        ('EE101', 'Electrical Engineering', 'Engineering'),
        ('CE101', 'Civil Engineering', 'Engineering'),
        ('ChE101', 'Chemical Engineering', 'Engineering'),
        ('CAE101', 'Control and Automation Engineering', 'Engineering'),
        ('CSE101', 'Computer Science Engineering', 'Computer Science')
    ]
    inserts = []
    for course in courses:
        inserts.append(f"INSERT INTO Course (course_id, course_name, department_name) VALUES ('{course[0]}', '{remove_accents(course[1])}', '{course[2]}');")
    return inserts, courses

def generate_student():
    courses = ['CS101', 'ME101', 'IE101', 'BA101', 'MA101', 'EE101', 'CE101', 'ChE101', 'CAE101', 'CSE101']
    students = []
    for i in range(1, 101):
        id = f'S{i:04d}'
        ssn = fake.ssn()
        name = fake.name()
        email = generate_email(name)
        course_id = random.choice(courses)
        students.append((id, ssn, name, email, course_id))
    inserts = []
    for student in students:
        inserts.append(f"INSERT INTO Student (ID, SSN, Name, Email, course_id) VALUES ('{student[0]}', '{student[1]}', '{remove_accents(student[2])}', '{student[3]}', '{student[4]}');")
    return inserts, students

def generate_subject():
    subjects = [
        ('DB101', 'Database Systems', 'Computer Science', 'CS101'),
        ('CA101', 'Calculus I', 'Mathematics', 'MA101'),
        ('SE101', 'Software Engineering', 'Computer Science', 'CS101'),
        ('LA101', 'Linear Algebra', 'Mathematics', 'MA101'),
        ('LO101', 'Logistics', 'Business Administration', 'BA101'),
        ('CA102', 'Control and Automation', 'Engineering', 'ME101'),
        ('P101', 'Programming I', 'Computer Science', 'CSE101'),
        ('P102', 'Programming II', 'Computer Science', 'CS101'),
        ('PH101', 'Physics I', 'Engineering', 'ME101'),
        ('PH102', 'Physics II', 'Engineering', 'ME101'),
        ('CH101', 'General Chemistry', 'Engineering', 'ChE101'),
        ('TH101', 'Thermodynamics', 'Engineering', 'EE101'),
        ('MS101', 'Strength of Materials', 'Engineering', 'CE101'),
        ('MF101', 'Fluid Mechanics', 'Engineering', 'CAE101'),
        ('CN101', 'Computer Networks', 'Computer Science', 'CSE101')
    ]
    inserts = []
    for subject in subjects:
        inserts.append(f"INSERT INTO Subject (subject_id, subject_name, department_name, course_id) VALUES ('{subject[0]}', '{remove_accents(subject[1])}', '{subject[2]}', '{subject[3]}');")
    return inserts, subjects

def generate_enrolled(students, curriculum_matrix):
    enrolled = []
    students_passed = random.sample(students, 6) 
    specific_students = [
        (students_passed[0], '2023-1', 2023),
        (students_passed[1], '2023-2', 2023),
    ]

    for student, semester, year in specific_students:
        course_id = student[4]
        course_subjects = [mat[1] for mat in curriculum_matrix if mat[0] == course_id]
        for subject_id in course_subjects:
            grade = 5.0
            status = 'Passed'
            enrolled.append((student[0], subject_id, semester, year, grade, status))

    for student in students:
        if student not in students_passed:
            course_id = student[4]
            course_subjects = [mat[1] for mat in curriculum_matrix if mat[0] == course_id]
            for subject_id in course_subjects:
                year = random.randint(2023, 2024)
                semester = f'{year}-{random.randint(1, 2)}'
                grade = round(random.uniform(0, 10), 1) if random.choice([True, False]) else 'NULL'
                if grade != 'NULL':
                    status = 'Passed' if grade > 5 else 'Failed'
                else:
                    status = 'Enrolled'
                enrolled.append((student[0], subject_id, semester, year, grade, status))

    inserts = []
    for enr in enrolled:
        grade_value = 'NULL' if enr[4] == 'NULL' else enr[4]
        inserts.append(f"INSERT INTO Enrolled (ID, subject_id, Semester, Year, Grade, status) VALUES ('{enr[0]}', '{enr[1]}', '{enr[2]}', {enr[3]}, {grade_value}, '{enr[5]}');")
    return inserts

def generate_teaches(subjects):
    professors = [f'P{i:03d}' for i in range(1, 26)]
    subject_ids = [subject[0] for subject in subjects]
    teaches = []
    subjects_current_semester = {subject: 0 for subject in subject_ids}

    for subject_id in subject_ids:
        for _ in range(random.randint(1, 2)):
            prof_id = random.choice(professors)
            semester = '2024-1'
            year = 2024
            status = 'Active'
            teaches.append((prof_id, subject_id, semester, year, status))
            subjects_current_semester[subject_id] += 1

    for _ in range(30):
        prof_id = random.choice(professors)
        subject_id = random.choice(subject_ids)
        year = random.randint(2023, 2023) 
        semester = f'{year}-{random.randint(1, 2)}'
        status = 'Inactive'
        teaches.append((prof_id, subject_id, semester, year, status))

    inserts = []
    for teach in teaches:
        inserts.append(f"INSERT INTO Teaches (ID_Prof, subject_id, Semester, Year, status) VALUES ('{teach[0]}', '{teach[1]}', '{teach[2]}', {teach[3]}, '{teach[4]}');")
    return inserts

def generate_advisor():
    students = [f'S{i:04d}' for i in range(1, 101)]
    professors = [f'P{i:03d}' for i in range(1, 26)]
    groups = []
    advisors = []
    group_id = 1

    for _ in range(25):
        num_members = random.randint(1, 4)
        members = random.sample(students, num_members)
        students = [student for student in students if student not in members]
        advisors.append((members, random.choice(professors), f'G{group_id:03d}'))
        group_id += 1

    inserts = []
    for adv in advisors:
        for student_id in adv[0]:
            inserts.append(f"INSERT INTO Advisor (student_id, prof_id, group_id) VALUES ('{student_id}', '{adv[1]}', '{adv[2]}');")
    return inserts

def generate_curriculum_matrix(courses, subjects):
    subjects_by_department = {
        'Computer Science': ['DB101', 'SE101', 'P101', 'P102', 'CN101'],
        'Engineering': ['CA102', 'PH101', 'PH102', 'CH101', 'TH101', 'MS101', 'MF101'],
        'Mathematics': ['CA101', 'LA101'],
        'Business Administration': ['LO101']
    }
    curriculum_matrix = []

    for course in courses:
        course_id, course_name, department_name = course
        dept = department_name
        valid_subjects = [s[0] for s in subjects if s[2] == dept or s[2] == 'Mathematics']
        if dept == 'Mathematics':
            valid_subjects += [s[0] for s in subjects if s[2] == 'Computer Science']
        selected_subjects = random.sample(valid_subjects, 3)
        for subject in selected_subjects:
            curriculum_matrix.append((course_id, subject))

    inserts = []
    for mat in curriculum_matrix:
        inserts.append(f"INSERT INTO CurriculumMatrix (course_id, subject_id) VALUES ('{mat[0]}', '{mat[1]}');")
    return inserts, curriculum_matrix

def generate_update_department_head(professors, departments):
    updates = []
    for dept in departments:
        profs_dept = [prof for prof in professors if prof[5] == dept[0]]
        if profs_dept:
            head = random.choice(profs_dept)[0]
            updates.append(f"UPDATE Department SET head_id = '{head}' WHERE department_name = '{dept[0]}';")
    return updates

def generate_data():
    with open('inserts.sql', 'w', encoding='utf-8') as f:
        f.write('-- Department\n')
        dept_inserts, departments = generate_department()
        for insert in dept_inserts:
            f.write(insert + '\n')

        f.write('-- Professor\n')
        prof_inserts, professors = generate_professor()
        for insert in prof_inserts:
            f.write(insert + '\n')

        f.write('-- Update Department Heads\n')
        update_inserts = generate_update_department_head(professors, departments)
        for update in update_inserts:
            f.write(update + '\n')

        f.write('-- Course\n')
        course_inserts, courses = generate_course()
        for insert in course_inserts:
            f.write(insert + '\n')

        f.write('-- Student\n')
        student_inserts, students = generate_student()
        for insert in student_inserts:
            f.write(insert + '\n')

        f.write('-- Subject\n')
        subject_inserts, subjects = generate_subject()
        for insert in subject_inserts:
            f.write(insert + '\n')

        f.write('-- Curriculum Matrix\n')
        matrix_inserts, curriculum_matrix = generate_curriculum_matrix(courses, subjects)
        for insert in matrix_inserts:
            f.write(insert + '\n')

        f.write('-- Enrolled\n')
        enrolled_inserts = generate_enrolled(students, curriculum_matrix)
        for insert in enrolled_inserts:
            f.write(insert + '\n')

        f.write('-- Teaches\n')
        teaches_inserts = generate_teaches(subjects)
        for insert in teaches_inserts:
            f.write(insert + '\n')

        f.write('-- Advisor\n')
        advisor_inserts = generate_advisor()
        for insert in advisor_inserts:
            f.write(insert + '\n')

if __name__ == "__main__":
    generate_data()
    print("Data generated and saved in 'inserts.sql'")
