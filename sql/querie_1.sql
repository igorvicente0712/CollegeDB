SELECT 
    s.subject_name AS "subject_name",
    e.Semester AS "Semester",
    e.Year AS "Year",
    e.Grade AS "Grade Final"
FROM 
    Enrolled e
JOIN 
    Subject s ON e.subject_id = s.subject_id
WHERE 
    e.ID = 'S0001'; 
