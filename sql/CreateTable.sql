CREATE TABLE Department (
    department_name VARCHAR(255) PRIMARY KEY,
    Budget INT,
    Building VARCHAR(50),
    head_id VARCHAR(10)
);

-- Professor Table
CREATE TABLE Professor (
    ID VARCHAR(10) PRIMARY KEY,
    SSN VARCHAR(11),
    Name VARCHAR(255),
    Email VARCHAR(255),
    Salary INT,
    department_name VARCHAR(255),
    FOREIGN KEY (department_name) REFERENCES Department(department_name)
);

-- Course Table
CREATE TABLE Course (
    course_id VARCHAR(10) PRIMARY KEY,
    course_name VARCHAR(255),
    department_name VARCHAR(255),
    FOREIGN KEY (department_name) REFERENCES Department(department_name)
);

-- Student Table
CREATE TABLE Student (
    ID VARCHAR(10) PRIMARY KEY,
    SSN VARCHAR(11),
    Name VARCHAR(255),
    Email VARCHAR(255),
    course_id VARCHAR(10),
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

-- Subject Table
CREATE TABLE Subject (
    subject_id VARCHAR(10) PRIMARY KEY,
    subject_name VARCHAR(255),
    department_name VARCHAR(255),
    course_id VARCHAR(10),
    FOREIGN KEY (department_name) REFERENCES Department(department_name),
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

-- Curriculum Matrix Table
CREATE TABLE CurriculumMatrix (
    course_id VARCHAR(10),
    subject_id VARCHAR(10),
    PRIMARY KEY (course_id, subject_id),
    FOREIGN KEY (course_id) REFERENCES Course(course_id),
    FOREIGN KEY (subject_id) REFERENCES Subject(subject_id)
);

-- Enrolled Table
CREATE TABLE Enrolled (
    ID VARCHAR(10),
    subject_id VARCHAR(10),
    Semester VARCHAR(10),
    Year INT,
    Grade DECIMAL(3,1),
    status VARCHAR(20),
    PRIMARY KEY (ID, subject_id, Semester, Year),
    FOREIGN KEY (ID) REFERENCES Student(ID),
    FOREIGN KEY (subject_id) REFERENCES Subject(subject_id)
);

-- Teaches Table
CREATE TABLE Teaches (
    ID_Prof VARCHAR(10),
    subject_id VARCHAR(10),
    Semester VARCHAR(10),
    Year INT,
    status VARCHAR(20),
    PRIMARY KEY (ID_Prof, subject_id, Semester, Year),
    FOREIGN KEY (ID_Prof) REFERENCES Professor(ID),
    FOREIGN KEY (subject_id) REFERENCES Subject(subject_id)
);

-- Advisor Table
CREATE TABLE Advisor (
    student_id VARCHAR(10),
    prof_id VARCHAR(10),
    group_id VARCHAR(10),
    PRIMARY KEY (student_id, prof_id),
    FOREIGN KEY (student_id) REFERENCES Student(ID),
    FOREIGN KEY (prof_id) REFERENCES Professor(ID)
);