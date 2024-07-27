import pyodbc
import streamlit as st

def connect_to_app_database():
    try:
        conn = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=CHRISTOFFERPC;"
            "Database=crud_test;"
            "Trusted_Connection=yes;"
        )
        print("Connected to the database successfully.")
        return conn
    except pyodbc.Error as e:
        st.error(f"Error connecting to application database: {e}")
        return None