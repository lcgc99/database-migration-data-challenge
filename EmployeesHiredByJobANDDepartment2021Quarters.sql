SELECT 	dp.Department, jb.Job, 
		SUM(CASE WHEN he.Datetime >= '2021-01-01' AND he.Datetime < '2021-04-01' THEN 1 ELSE 0 END) "Q1",
		SUM(CASE WHEN he.Datetime >= '2021-04-01' AND he.Datetime < '2021-07-01' THEN 1 ELSE 0 END) "Q2",
		SUM(CASE WHEN he.Datetime >= '2021-07-01' AND he.Datetime < '2021-10-01' THEN 1 ELSE 0 END) "Q3",
		SUM(CASE WHEN he.Datetime >= '2021-10-01' AND he.Datetime < '2022-01-01' THEN 1 ELSE 0 END) "Q4"
FROM 	HIRED_EMPLOYEES 								he
JOIN	DEPARTMENTS 									dp 
	ON	he.DepartmentId = dp.Id 
JOIN	JOBS 											jb
	ON	he.JobId = jb.Id 							
WHERE 	he.Datetime >= '2021-01-01'
	AND	he.Datetime <  '2022-01-01'
GROUP BY	dp.Department, jb.Job 
