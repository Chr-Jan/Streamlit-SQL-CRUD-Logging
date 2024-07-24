import pyodbc
import streamlit as st

def create_people_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            IF OBJECT_ID('dbo.people', 'U') IS NULL
            CREATE TABLE people (
                id INT IDENTITY(1,1) PRIMARY KEY,
                name VARCHAR(50),
                age INT,
                age_plus_two AS (age + 2)
            )
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
            CREATE TABLE logs (
                log_id INT IDENTITY(1,1) PRIMARY KEY,
                user_id INT,
                username VARCHAR(50),
                action VARCHAR(255),
                timestamp DATETIME
            )
            """
        )
        conn.commit()
        print("Table 'logs' created or already exists.")
    except pyodbc.Error as e:
        print(f"Error creating 'logs' table: {e}")

def create_user_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            IF OBJECT_ID('dbo.users', 'U') IS NULL
            CREATE TABLE users (
                user_id INT IDENTITY(1,1) PRIMARY KEY,
                username VARCHAR(50),
                password VARCHAR(50)
            )
            """
        )
        conn.commit()
        print("Table 'users' created or already exists.")
    except pyodbc.Error as e:
        print(f"Error creating 'users' table: {e}")

def create_roles_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            IF OBJECT_ID('dbo.roles', 'U') IS NULL
            CREATE TABLE roles (
                role_id INT IDENTITY(1,1) PRIMARY KEY,
                role_name VARCHAR(50)
            )
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
        users = [('admin', 'password'), ('user', 'password')]

        for username, password in users:
            # Check if the user already exists
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
            if cursor.fetchone()[0] == 0:
                # Insert if user does not exist
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        
        conn.commit()
        print("Default users inserted if they did not already exist.")
    except pyodbc.Error as e:
        print(f"Error inserting default users: {e}")

