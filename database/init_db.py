import pyodbc
import streamlit as st

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
            CREATE TABLE users (
                id INT IDENTITY(1,1) PRIMARY KEY,
                name VARCHAR(50),
                age INT
            )
        """)
        conn.commit()
    except pyodbc.Error as e:
        st.error(f"Error creating users table: {e}")

def create_log_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='logs' AND xtype='U')
            CREATE TABLE logs (
                log_id INT IDENTITY(1,1) PRIMARY KEY,
                user_id INT,
                username VARCHAR(50),
                action TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    except pyodbc.Error as e:
        st.error(f"Error creating logs table: {e}")
