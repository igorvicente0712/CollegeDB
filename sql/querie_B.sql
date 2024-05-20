SELECT 
    s.subject_name AS "Disciplina",
    t.Semester AS "Semester",
    t.Year AS "Year"
FROM 
    Teaches t
JOIN 
    Subject s ON t.subject_id = s.subject_id
WHERE 
    t.ID_Prof = 'P001';
