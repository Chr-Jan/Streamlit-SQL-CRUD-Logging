import pyodbc
import streamlit as st
from utils.logger import get_logger

logger = get_logger()

def insert_data(conn, name, age):
    try:
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO users (name, age) VALUES ('{name}', {age})")
        conn.commit()
        st.success(f"Inserted '{name}' with age {age} into 'users' table")
        logger.info(f"Inserted '{name}' with age {age}")
    except pyodbc.Error as e:
        st.error(f"Error inserting data: {e}")
        logger.error(f"Error inserting data: {e}")

def get_all_data(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows
    except pyodbc.Error as e:
        st.error(f"Error retrieving data: {e}")
        logger.error(f"Error retrieving data: {e}")
        return None

def update_data(conn, user_id, name, age):
    try:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET name = '{name}', age = {age} WHERE id = {user_id}")
        conn.commit()
        st.success(f"Updated user with ID {user_id} in 'users' table")
        logger.info(f"Updated user with ID {user_id} to name '{name}' and age {age}")
    except pyodbc.Error as e:
        st.error(f"Error updating data: {e}")
        logger.error(f"Error updating data: {e}")

def delete_data(conn, user_id):
    try:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM users WHERE id = {user_id}")
        conn.commit()
        st.success(f"Deleted user with ID {user_id} from 'users' table")
        logger.info(f"Deleted user with ID {user_id}")
    except pyodbc.Error as e:
        st.error(f"Error deleting data: {e}")
        logger.error(f"Error deleting data: {e}")
