# Streamlit-SQL-CRUD-Operations

## Usefull SQL Quories I have been using
´´´
-- CREATE DATABASE crud_test
-- GO

-- USE crud_test
-- GO

/*
CREATE TABLE users (
	id INT PRIMARY KEY IDENTITY(1,1), 
	name varchar(50), 
	email varchar(50)
);
*/

-- SELECT * FROM users;

-- SELECT @@SERVERNAME

-- ALTER TABLE users
-- DROP COLUMN email;

-- ALTER TABLE users
-- ADD age INT;

-- ALTER TABLE users
-- DROP COLUMN age;

--ALTER TABLE users
-- ADD age INT CHECK (age >= 0 AND age <= 150);
´´´