import pyodbc
import streamlit as st
from datetime import datetime
from core.connection import connect_to_app_database

def log_action(username, user_id, action):
    log_conn = connect_to_app_database()
    if log_conn:
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor = log_conn.cursor()
            cursor.execute(
                "INSERT INTO dbo.log_people (user_id, username, action, timestamp) VALUES (?, ?, ?, ?)",
                (user_id, username, action, timestamp)
            )
            log_conn.commit()
        except pyodbc.Error as e:
            st.error(f"Error logging action: {e}")

def get_all_data_people(conn, table="people"):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        return rows
    except pyodbc.Error as e:
        st.error(f"Error retrieving data: {e}")
        return None

def insert_data(conn, username, name, age):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO people (name, age) VALUES (?, ?)", (name, age))
        conn.commit()
        
        cursor.execute("SELECT SCOPE_IDENTITY()")
        user_id = cursor.fetchone()[0]
        
        st.success(f"Inserted '{name}' with age {age} into 'people' table")
        log_action(username, user_id, f"Inserted '{name}' with age {age}")
    except pyodbc.Error as e:
        st.error(f"Error inserting data: {e}")

def update_data(conn, username, user_id, name, age):
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE people SET name = ?, age = ? WHERE user_id = ?", (name, age, user_id))
        conn.commit()
        st.success(f"Updated user with ID {user_id} in 'people' table")
        log_action(username, user_id, f"Updated user with ID {user_id} to name '{name}' and age {age}")
    except pyodbc.Error as e:
        st.error(f"Error updating data: {e}")

def delete_data(conn, username, user_id):
    try:
        cursor = conn.cursor()

        # Check if the user exists in the 'people' table
        cursor.execute("SELECT COUNT(*) FROM people WHERE people_id = ?", (user_id,))
        if cursor.fetchone()[0] == 0:
            st.error(f"User with ID {user_id} does not exist in 'people' table.")
            return

        # Delete the user from the 'people' table
        cursor.execute("DELETE FROM people WHERE people_id = ?", (user_id,))
        conn.commit()
        st.success(f"Deleted user with ID {user_id} from 'people' table")
        
        # Log the action
        log_action(username, user_id, f"Deleted user with ID {user_id}")
        
    except pyodbc.Error as e:
        st.error(f"Error deleting data: {e}")
