import pyodbc
import streamlit as st
from core.connection import connect_to_app_database

def register_user(username, password, role_name):
    conn = connect_to_app_database()
    if conn:
        try:
            cursor = conn.cursor()

            # Fetch role_id from role_name
            cursor.execute("SELECT role_id FROM roles WHERE role_name = ?", (role_name,))
            role_id = cursor.fetchone()[0]

            # Check if the username already exists
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
            if cursor.fetchone()[0] > 0:
                st.error(f"Username '{username}' already exists.")
                return

            # Insert new user
            cursor.execute("INSERT INTO users (username, password, role_id) VALUES (?, ?, ?)", (username, password, role_id))
            conn.commit()
            st.success(f"User '{username}' registered successfully!")
        except pyodbc.Error as e:
            st.error(f"Error registering user: {e}")
        finally:
            conn.close()

# Simple authentication function
def authenticate(username, password):
    if username == "admin" and password == "password":
        st.session_state['role'] = 'admin'
        return True
    elif username == "user" and password == "password":
        st.session_state['role'] = 'user'
        return True
    else:
        return False

def authenticate(username, password):
    conn = connect_to_app_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT password, role_id FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            
            if result and result[0] == password:
                role_id = result[1]
                
                cursor.execute("SELECT role_name FROM roles WHERE role_id = ?", (role_id,))
                role_name = cursor.fetchone()[0]
                
                st.session_state['role'] = role_name
                return True
            else:
                return False
        except pyodbc.Error as e:
            st.error(f"Error authenticating user: {e}")
            return False
        finally:
            conn.close()
    else:
        st.error("Failed to connect to the database.")
        return False