WITH PassedSubjects AS (
    SELECT e.ID AS student_id, e.subject_id, e.Grade, e.status
    FROM Enrolled e
    WHERE e.Grade >= 5 AND e.status = 'Passed'
),
CurriculumSubjects AS (
    SELECT cm.course_id, cm.subject_id
    FROM CurriculumMatrix cm
),
GraduatedStudents AS (
    SELECT s.ID AS student_id, s.Name AS student_name, s.course_id
    FROM Student s
    JOIN CurriculumSubjects cs ON s.course_id = cs.course_id
    LEFT JOIN PassedSubjects ps ON s.ID = ps.student_id AND cs.subject_id = ps.subject_id
    GROUP BY s.ID, s.Name, s.course_id
    HAVING COUNT(DISTINCT cs.subject_id) = COUNT(DISTINCT ps.subject_id)
)
SELECT gs.student_id, gs.student_name, gs.course_id, e.Semester, e.Year, e.Grade, e.status
FROM GraduatedStudents gs
JOIN Enrolled e ON gs.student_id = e.ID
WHERE e.Semester = '2023-1' AND e.Year = 2023
GROUP BY gs.student_id, gs.student_name, gs.course_id, e.Semester, e.Year, e.Grade, e.status;
