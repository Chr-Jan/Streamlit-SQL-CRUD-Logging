import pyodbc
import streamlit as st

def connect_to_database():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=ChristofferPC;" 
            "Database=crud_test;" 
            "Trusted_Connection=yes;"
        )
        return conn
    except pyodbc.Error as ex:
        st.error(f"Error connecting to the database: {ex}")
        return None