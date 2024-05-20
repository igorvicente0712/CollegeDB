SELECT p.Name AS ProfessorName, d.department_name AS DepartmentName
FROM Professor p
JOIN Department d ON p.department_name = d.department_name
WHERE p.ID = d.head_id;
