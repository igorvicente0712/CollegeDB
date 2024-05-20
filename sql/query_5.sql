SELECT s.Name AS student_name, p.Name AS advisor_name, a.group_id
FROM Student s
JOIN Advisor a ON s.ID = a.student_id
JOIN Professor p ON a.prof_id = p.ID;
