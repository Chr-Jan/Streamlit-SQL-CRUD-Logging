import pyodbc
import streamlit as st

def connect_to_app_database():
    try:
        conn = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=ChristofferPC;"
            "Database=crud_test;"
            "Trusted_Connection=yes;"
        )
        return conn
    except pyodbc.Error as e:
        st.error(f"Error connecting to application database: {e}")
        return None

def connect_to_log_database():
    try:
        conn = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=ChristofferPC;"
            "Database=crud_test;"
            "Trusted_Connection=yes;"
        )
        return conn
    except pyodbc.Error as e:
        st.error(f"Error connecting to log database: {e}")
        return None
