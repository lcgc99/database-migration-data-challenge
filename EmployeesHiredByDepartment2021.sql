WITH	EmployeesHiredByDepartment2021 AS (
	SELECT 	dp.Id, dp.Department, COUNT(1) "HiredEmployees"
	FROM 	HIRED_EMPLOYEES 									            he
	JOIN	DEPARTMENTS 										            dp
		ON	he.DepartmentId = dp.Id
	WHERE 	he.Datetime >= '2021-01-01'
		AND	he.Datetime <  '2022-01-01'
	GROUP BY	dp.Id, dp.Department 
)
SELECT 	Id, Department, HiredEmployees
FROM 	EmployeesHiredByDepartment2021
WHERE 	HiredEmployees > (SELECT AVG(HiredEmployees) FROM EmployeesHiredByDepartment2021)
ORDER BY	HiredEmployees DESC
