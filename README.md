# Streamlit-SQL-CRUD-Operations

This project demonstrates basic CRUD (Create, Read, Update, Delete) operations using Streamlit for a SQL Server database. It allows users to interact with a database through a web interface built with Streamlit, making it easy to manage user data.

## Functionality
* Create User: Allows inserting a new user with name and age into the database.
* View Users: Displays all users currently stored in the database.
* Update User: Updates the name and age of an existing user in the database.
* Delete User: Removes a user from the database based on their ID.

## How It Works
* Connection to Database: Establishes a connection to a SQL Server database using pyodbc.
* CRUD Operations: Each operation (Create, Read, Update, Delete) is handled through functions interacting with the database.
* Session State: Uses Streamlit's session_state to maintain the database connection across different interactions without reconnecting unnecessarily.

## Usefull SQL Quories I have been using
### Creating Database and Table
<pre><code>
CREATE DATABASE crud_test
GO
</code></pre>
<pre><code>
USE crud_test
GO
</code></pre>
<pre><code>
CREATE TABLE users (
    id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(50),
    age INT
);
</code></pre>

<h3>Retrieving Data</h3>
<pre><code>
SELECT * FROM users;
</code></pre>
<pre><code>
SELECT @@SERVERNAME;
</code></pre>

<h3>Modifying Table Structure</h3>
<pre><code>
ALTER TABLE users
DROP COLUMN email;
</code></pre>
<pre><code>
ALTER TABLE users
ADD age INT;
</code></pre>
<pre><code>
ALTER TABLE users
DROP COLUMN age;
</code></pre>
<pre><code>
ALTER TABLE users
ADD age INT CHECK (age >= 0 AND age <= 150);
</code></pre>
