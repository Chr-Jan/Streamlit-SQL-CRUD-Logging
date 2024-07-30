# Streamlit SQL / CRUD / Logging - Operations

This project showcases basic CRUD (Create, Read, Update, Delete) operations using Streamlit to interact with a SQL Server database. It provides a user-friendly web interface for managing user data efficiently, along with logging functionalities to track user actions.

## Functionality
- <b>Create User:</b> Insert a new user with name and age into the database.
- <b>View Users:</b> Display all users currently stored in the database.
- <b>Update User:</b> Modify the name and age of an existing user.
- <b>Delete User:</b> Remove a user from the database based on their ID.

### Logging
- <strong>Action Logging:</strong> Logs user actions such as user creation, updates, and deletions, capturing details like username, user ID, action performed, and timestamp.

## How It Works
<ul>
        <li><strong>Connection to Database:</strong> Establishes a connection to a SQL Server database using pyodbc.</li>
        <li><strong>CRUD Operations:</strong> Each operation is managed through dedicated functions interacting directly with the database.</li>
        <li><strong>Session State Management:</strong> Utilizes Streamlit's session_state feature to maintain the database connection across different interactions, improving performance and usability.</li>
    </ul>

## Useful Links

www.draw.io

## Useful SQL Queries

### Creating Database and Table
<pre><code>CREATE DATABASE crud_test;
USE crud_test;
CREATE TABLE users (
    id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(50),
    age INT
);</code></pre>

### Retrieving Data
<pre><code>SELECT * FROM users;
SELECT @@SERVERNAME;</code></pre>

### Modifying Table Structure
<pre><code>ALTER TABLE users
DROP COLUMN age;
ALTER TABLE users
ADD email VARCHAR(50);
ALTER TABLE users
DROP COLUMN email;
ALTER TABLE users
ADD age INT CHECK (age >= 0 AND age <= 150);</code></pre>
