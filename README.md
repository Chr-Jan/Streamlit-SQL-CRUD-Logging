<h1>Streamlit-SQL-CRUD-Operations</h1>

This project showcases basic CRUD (Create, Read, Update, Delete) operations using Streamlit to interact with a SQL Server database. It provides a user-friendly web interface for managing user data efficiently, along with logging functionalities to track user actions.

## Functionality
<ul>
        <li><strong>Create User:</strong> Insert a new user with name and age into the database.</li>
        <li><strong>View Users:</strong> Display all users currently stored in the database.</li>
        <li><strong>Update User:</strong> Modify the name and age of an existing user.</li>
        <li><strong>Delete User:</strong> Remove a user from the database based on their ID.</li>
</ul>

### Logging
- <strong>Action Logging:</strong> Logs user actions such as user creation, updates, and deletions, capturing details like username, user ID, action performed, and timestamp.

## How It Works
<ul>
        <li><strong>Connection to Database:</strong> Establishes a connection to a SQL Server database using pyodbc.</li>
        <li><strong>CRUD Operations:</strong> Each operation is managed through dedicated functions interacting directly with the database.</li>
        <li><strong>Session State Management:</strong> Utilizes Streamlit's session_state feature to maintain the database connection across different interactions, improving performance and usability.</li>
    </ul>

## Useful SQL Queries

<h3>Creating Database and Table</h3>
    <pre><code>CREATE DATABASE crud_test;
USE crud_test;
CREATE TABLE users (
    id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(50),
    age INT
);</code></pre>

<h3>Retrieving Data</h3>
    <pre><code>SELECT * FROM users;
SELECT @@SERVERNAME;</code></pre>

<h3>Modifying Table Structure</h3>
    <pre><code>ALTER TABLE users
DROP COLUMN age;
ALTER TABLE users
ADD email VARCHAR(50);
ALTER TABLE users
DROP COLUMN email;
ALTER TABLE users
ADD age INT CHECK (age >= 0 AND age <= 150);</code></pre>
