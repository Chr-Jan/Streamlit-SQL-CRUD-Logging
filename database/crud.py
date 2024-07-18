import pyodbc
import streamlit as st
from database.connection import connect_to_log_database

def log_action(username, user_id, action):
    log_conn = connect_to_log_database()
    if log_conn:
        try:
            cursor = log_conn.cursor()
            cursor.execute("INSERT INTO logs (username, user_id, action) VALUES (?, ?, ?)", (username, user_id, action))
            log_conn.commit()
        except pyodbc.Error as e:
            st.error(f"Error logging action: {e}")

def insert_data(conn, username, name, age):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
        conn.commit()
        
        # Get the last inserted ID using SCOPE_IDENTITY()
        cursor.execute("SELECT SCOPE_IDENTITY()")
        user_id = cursor.fetchone()[0]
        
        st.success(f"Inserted '{name}' with age {age} into 'users' table")
        log_action(username, user_id, f"Inserted '{name}' with age {age}")
    except pyodbc.Error as e:
        st.error(f"Error inserting data: {e}")

def get_all_data(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows
    except pyodbc.Error as e:
        st.error(f"Error retrieving data: {e}")
        return None

def update_data(conn, username, user_id, name, age):
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET name = ?, age = ? WHERE id = ?", (name, age, user_id))
        conn.commit()
        st.success(f"Updated user with ID {user_id} in 'users' table")
        log_action(username, user_id, f"Updated user with ID {user_id} to name '{name}' and age {age}")
    except pyodbc.Error as e:
        st.error(f"Error updating data: {e}")

def delete_data(conn, username, user_id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        st.success(f"Deleted user with ID {user_id} from 'users' table")
        log_action(username, user_id, f"Deleted user with ID {user_id}")
    except pyodbc.Error as e:
        st.error(f"Error deleting data: {e}")
