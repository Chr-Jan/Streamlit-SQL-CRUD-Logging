import pyodbc
import streamlit as st

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT PRIMARY KEY,
                name VARCHAR(50),
                age INT
            )
        """)
        conn.commit()
    except pyodbc.Error as e:
        st.error(f"Error creating table: {e}")