CREATE DATABASE edupluse;

USE edupluse;


UPDATE student
SET `Application mode` = REPLACE(
`Application mode`,
    'â€”',
    ' — '
)
WHERE `Application mode` LIKE '%â€”%';

UPDATE student
SET `Mothers qualification` = REPLACE(
`Mothers qualification`,
    'â€”',
    ' — '
)
WHERE `Mothers qualification` LIKE '%â€”%';

UPDATE student
SET `Fathers qualification` = REPLACE(
`Fathers qualification`,
    'â€”',
    ' — '
)
WHERE `Fathers qualification` LIKE '%â€”%';

ALTER TABLE student
ADD COLUMN student_id INT AUTO_INCREMENT PRIMARY KEY FIRST;

SELECT COUNT(*) FROM student;

SELECT * FROM student
LIMIT 5;

-- Q 1. What is the overall distribution of students by academic outcome?
SELECT Target,
COUNT(student_id) AS `Total Student`,
ROUND(COUNT(student_id) * 100.0 / (SELECT COUNT(*) FROM student),2) AS Percentage 
FROM student
GROUP BY Target;

-- Q 2. Are students with outstanding debt more likely to drop out?
SELECT
    Debtor,
    COUNT(*) AS `Total Students`,
    SUM(Target = 'Dropout') AS `Dropout Students`,
    ROUND(
        SUM(Target = 'Dropout') * 100.0 / COUNT(*),
        2
    ) AS `Dropout Rate`
FROM student
GROUP BY Debtor
ORDER BY `Dropout Rate` DESC;

-- Q 3. Are students who are not up to date with their tuition fees more likely to drop out?
SELECT `Tuition fees up to date`,
COUNT(*) AS `Total Students`,
SUM(Target = 'Dropout') AS `Dropout Students`,
ROUND(
        SUM(Target = 'Dropout') * 100.0 / COUNT(*),
        2
    ) AS `Dropout Rate`
FROM student
GROUP BY `Tuition fees up to date`
ORDER BY `Dropout Rate` DESC;

-- Q 4. Is dropout rate different between scholarship holders and non-scholarship students?
SELECT `Scholarship holder`,COUNT(*) AS `Total Students`,
SUM(Target = 'Dropout') AS `Dropout Students`,
ROUND(SUM(Target = 'Dropout') * 100.0 / COUNT(*),2) AS 
`Dropout Rate`
FROM student
GROUP BY `Scholarship holder`
ORDER BY `Dropout Rate` DESC;

-- Q 5. Does dropout rate vary significantly across different courses?
SELECT
    Course,
    COUNT(*) AS `Total Students`,
    SUM(Target = 'Dropout') AS `Dropout Students`,
    ROUND(
        SUM(Target = 'Dropout') * 100.0 / COUNT(*),
        2
    ) AS `Dropout Rate`
FROM student
GROUP BY Course
ORDER BY `Dropout Rate` DESC;

-- Q 6. Is dropout rate different between daytime and evening students?
SELECT
    `Daytime/evening attendance`,
    COUNT(*) AS `Total Students`,
    SUM(Target = 'Dropout') AS `Dropout Students`,
    ROUND(
        SUM(Target = 'Dropout') * 100.0 / COUNT(*),
        2
    ) AS `Dropout Rate`
FROM student
GROUP BY `Daytime/evening attendance`
ORDER BY `Dropout Rate` DESC;

-- Q 7. Do students with lower academic performance have a higher dropout rate?
SELECT Target,
ROUND(AVG(`Curricular units 2nd sem (grade)`),2) AS `Average Grade`
FROM student
GROUP BY Target
ORDER BY `Average Grade` ASC;

-- Q 8. Do dropout students successfully complete fewer curricular units in the 2nd semester than graduate students?
SELECT Target,
ROUND(AVG(`Curricular units 2nd sem (approved)`),2) AS `Average Unit`
FROM student
GROUP BY Target
ORDER BY `Average Unit` ASC;

-- Q 9. Do dropout students have more curricular units without evaluation than graduate students?
SELECT Target,
ROUND(AVG(`Curricular units 2nd sem (without evaluations)`),2) AS `Average Unit(Without Evaluations)`
FROM student
GROUP BY Target
ORDER BY `Average Unit(Without Evaluations)` ASC;

-- Q 10. Is dropout rate different across student age groups?

ALTER TABLE student
ADD COLUMN `Age Group` VARCHAR(20);

UPDATE student
SET `Age Group` =
    CASE
        WHEN `Age at enrollment` BETWEEN 17 AND 20 THEN '17-20'
        WHEN `Age at enrollment` BETWEEN 21 AND 24 THEN '21-24'
        WHEN `Age at enrollment` BETWEEN 25 AND 29 THEN '25-29'
        WHEN `Age at enrollment` >= 30 THEN '30+'
    END;
    
SELECT 
    `Age Group`,
    COUNT(*) AS `Total Students`,
    SUM(Target = 'Dropout') AS `Dropout Students`,
    ROUND(SUM(Target = 'Dropout') * 100.0 / COUNT(*),2) AS `Drop Rate`
FROM student
GROUP BY  `Age Group`
ORDER BY `Age Group`;

-- Q 11. Is dropout rate different between male and female students?
SELECT 
    Gender,
    COUNT(*) AS `Total Students`,
    SUM(Target = 'Dropout') AS `Dropout Students`,
    ROUND(SUM(Target = 'Dropout') * 100.0 / COUNT(*),2) AS `Drop Rate`
FROM student
GROUP BY  Gender
ORDER BY `Drop Rate` DESC;

-- Q 12. Is dropout rate different between international and non-international students?
SELECT 
    International,
    COUNT(*) AS `Total Students`,
    SUM(Target = 'Dropout') AS `Dropout Students`,
    ROUND(SUM(Target = 'Dropout') * 100.0 / COUNT(*),2) AS `Drop Rate`
FROM student
GROUP BY  International
ORDER BY `Drop Rate` DESC;

-- Q 13. Do dropout students have fewer approved curricular units in the 1st semester than graduate students?
SELECT Target,
ROUND(AVG(`Curricular units 1st sem (approved)`),2) AS `Average Unit`
FROM student
GROUP BY Target
ORDER BY `Average Unit` ASC;

-- Q 14. Is the academic performance difference between Dropout and Graduate students already visible in the 1st semester?
SELECT Target,
ROUND(AVG(`Curricular units 1st sem (grade)`),2) AS `Average 1st sem Grade`,
ROUND(AVG(`Curricular units 2nd sem (grade)`),2) AS `Average 2nd sem Grade`
FROM student
GROUP BY Target;

-- Q 15. Do students with financial difficulties AND weaker academic progress show a higher observed dropout rate?
SELECT Debtor,Target,
ROUND(AVG(`Curricular units 1st sem (grade)`),2) AS `Average 1st sem Grade`,
ROUND(AVG(`Curricular units 2nd sem (grade)`),2) AS `Average 2nd sem Grade`
FROM student
GROUP BY Debtor,Target;

-- Q 16. What is the dropout rate for students who have both financial difficulty and weaker academic performance?
SELECT COUNT(*) AS `Total Students` ,
SUM(Target = 'Dropout') AS `Dropout Students`,
ROUND(SUM(Target = 'Dropout') * 100.0 / COUNT(*),2) AS `Dropout Rate`
FROM student
WHERE  Debtor = 'Yes' AND `Curricular units 2nd sem (grade)` < 8;

-- Q 17. Among students with weaker academic performance, does financial difficulty further change the observed dropout rate?
SELECT Debtor , COUNT(*) AS `Total Students` ,
SUM(Target = 'Dropout') AS `Dropout Students`,
ROUND(SUM(Target = 'Dropout') * 100.0 / COUNT(*),2) AS `Dropout Rate`
FROM student
WHERE (`Curricular units 2nd sem (grade)` < 8)
GROUP BY Debtor
ORDER BY `Dropout Rate` DESC;

-- Q 18.What is the strongest observed difference between Dropout and Graduate students that could be useful for student-retention action?
SELECT
    Target,
    COUNT(*) AS `Total Students`,
    ROUND(AVG(`Curricular units 1st sem (grade)`), 2) AS `Avg 1st Sem Grade`,
    ROUND(AVG(`Curricular units 2nd sem (grade)`), 2) AS `Avg 2nd Sem Grade`,
    ROUND(AVG(`Curricular units 1st sem (approved)`), 2) AS `Avg 1st Sem Approved`,
    ROUND(AVG(`Curricular units 2nd sem (approved)`), 2) AS `Avg 2nd Sem Approved`,
    ROUND(AVG(`Curricular units 1st sem (without evaluations)`), 2) AS `Avg 1st Sem Without Evaluation`,
    ROUND(AVG(`Curricular units 2nd sem (without evaluations)`), 2) AS `Avg 2nd Sem Without Evaluation`
FROM student
WHERE Target IN ('Dropout', 'Graduate')
GROUP BY Target;


