import pyodbc
import streamlit as st

def create_people_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            IF OBJECT_ID('dbo.people', 'U') IS NULL
            BEGIN
                CREATE TABLE people (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    name VARCHAR(50),
                    age INT,
                    age_plus_two AS (age + 2)
                )
            END
            """
        )
        conn.commit()
        print("Table 'people' created or already exists.")
    except pyodbc.Error as e:
        print(f"Error creating 'people' table: {e}")

def create_log_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            IF OBJECT_ID('dbo.logs', 'U') IS NULL
            BEGIN
                CREATE TABLE logs (
                    log_id INT IDENTITY(1,1) PRIMARY KEY,
                    user_id INT,
                    username VARCHAR(50),
                    action VARCHAR(255),
                    timestamp DATETIME,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            END
            """
        )
        conn.commit()
        print("Table 'logs' created or already exists.")
    except pyodbc.Error as e:
        print(f"Error creating 'logs' table: {e}")

def create_food_production_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            IF OBJECT_ID('dbo.food_production', 'U') IS NULL
            BEGIN
                CREATE TABLE dbo.food_production (
                    production_id INT IDENTITY(1,1) PRIMARY KEY,
                    food_name VARCHAR(50),
                    production_date DATE,
                    quantity INT,
                    goal_reacted BIT,
                    CONSTRAINT ck_goal_reacted_ischk CHECK (goal_reacted IN (0, 1))
                )
            END
            """
        )
        conn.commit()
        print("Table 'food_production' created or already exists.")
    except pyodbc.Error as e:
        print(f"Error creating 'food_production' table: {e}")

def create_user_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            IF OBJECT_ID('dbo.users', 'U') IS NULL
            BEGIN
                CREATE TABLE users (
                    user_id INT IDENTITY(1,1) PRIMARY KEY,
                    username VARCHAR(50),
                    password VARCHAR(50),
                    role_id INT,
                    FOREIGN KEY (role_id) REFERENCES roles(role_id)
                )
            END
            """
        )
        conn.commit()
        print("Table 'users' created or already exists.")
    except pyodbc.Error as e:
        print(f"Error creating 'users' table: {e}")

def create_roles_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            IF OBJECT_ID('dbo.roles', 'U') IS NULL
            BEGIN
                CREATE TABLE roles (
                    role_id INT IDENTITY(1,1) PRIMARY KEY,
                    role_name VARCHAR(50)
                )
            END
            """
        )
        conn.commit()
        print("Table 'roles' created or already exists.")
    except pyodbc.Error as e:
        print(f"Error creating 'roles' table: {e}")

def insert_default_roles(conn):
    try:
        cursor = conn.cursor()
        roles = ['admin', 'user']

        for role in roles:
            # Check if the role already exists
            cursor.execute("SELECT COUNT(*) FROM roles WHERE role_name = ?", (role,))
            if cursor.fetchone()[0] == 0:
                # Insert if role does not exist
                cursor.execute("INSERT INTO roles (role_name) VALUES (?)", (role,))
        
        conn.commit()
        print("Default roles inserted if they did not already exist.")
    except pyodbc.Error as e:
        print(f"Error inserting default roles: {e}")

def insert_default_users(conn):
    try:
        cursor = conn.cursor()

        # First, retrieve the role IDs for 'admin' and 'user'
        cursor.execute("SELECT role_id FROM roles WHERE role_name = 'admin'")
        admin_role_id = cursor.fetchone()[0]

        cursor.execute("SELECT role_id FROM roles WHERE role_name = 'user'")
        user_role_id = cursor.fetchone()[0]

        users = [
            ('admin', 'password', admin_role_id),
            ('user', 'password', user_role_id)
        ]

        for username, password, role_id in users:
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO users (username, password, role_id) VALUES (?, ?, ?)", (username, password, role_id))
        
        conn.commit()
        print("Default users inserted if they did not already exist.")
    except pyodbc.Error as e:
        print(f"Error inserting default users: {e}")

def seed_food_production_table(conn):
    try:
        cursor = conn.cursor()
        cursor.executemany(
            """
            INSERT INTO dbo.food_production (food_name, production_date, quantity, goal_reacted)
            VALUES (?, ?, ?, ?)
            """,
            [
                ('Apples', '2024-01-15', 150, 1),
                ('Bananas', '2024-02-10', 200, 0),
                ('Carrots', '2024-03-05', 300, 1),
                ('Potatoes', '2024-04-20', 400, 0),
                ('Tomatoes', '2024-05-15', 250, 1)
            ]
        )
        conn.commit()
        print("Seed data inserted into 'food_production' table.")
    except pyodbc.Error as e:
        print(f"Error inserting seed data into 'food_production' table: {e}")
