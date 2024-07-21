import pyodbc
import streamlit as st

def create_people_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='people' AND xtype='U')
            CREATE TABLE people (
                id INT IDENTITY(1,1) PRIMARY KEY,
                name VARCHAR(50),
                age INT
            )
        """)
        conn.commit()
        st.success("Table 'people' created or already exists.")
    except pyodbc.Error as e:
        st.error(f"Error creating 'people' table: {e}")

def create_log_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='logs' AND xtype='U')
            CREATE TABLE logs (
                log_id INT IDENTITY(1,1) PRIMARY KEY,
                user_id INT,
                username VARCHAR(50),
                action VARCHAR(255),
                timestamp DATETIME
            )
        """)
        conn.commit()
        st.success("Table 'logs' created or already exists.")
    except pyodbc.Error as e:
        st.error(f"Error creating 'logs' table: {e}")

def create_user_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
            CREATE TABLE users (
                user_id INT IDENTITY(1,1) PRIMARY KEY,
                username VARCHAR(50),
                password VARCHAR(50)
            )
        """)
        conn.commit()
        st.success("Table 'users' created or already exists.")
    except pyodbc.Error as e:
        st.error(f"Error creating 'users' table: {e}")

def create_roles_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='roles' AND xtype='U')
            CREATE TABLE roles (
                role_id INT IDENTITY(1,1) PRIMARY KEY,
                role_name VARCHAR(50)
            )
        """)
        conn.commit()
        st.success("Table 'roles' created or already exists.")
    except pyodbc.Error as e:
        st.error(f"Error creating 'roles' table: {e}")

def insert_default_roles(conn):
    try:
        cursor = conn.cursor()
        roles = ['admin', 'user']
        for role in roles:
            cursor.execute("INSERT INTO roles (role_name) VALUES (?)", (role,))
        conn.commit()
        st.success("Default roles inserted.")
    except pyodbc.Error as e:
        st.error(f"Error inserting default roles: {e}")

def insert_default_users(conn):
    try:
        cursor = conn.cursor()
        users = [('admin', 'password'), ('user', 'password')]
        for username, password in users:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        st.success("Default users inserted.")
    except pyodbc.Error as e:
        st.error(f"Error inserting default users: {e}")
