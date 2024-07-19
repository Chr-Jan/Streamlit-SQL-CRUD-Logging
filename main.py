import pyodbc
import streamlit as st
from database.connection import connect_to_app_database
from database.init_db import create_table, create_log_table
from database.crud import insert_data, get_all_data, update_data, delete_data, log_action

# Simple authentication function
def authenticate(username, password):
    # Hardcoded credentials (replace with database lookup in real scenario)
    if username == "admin" and password == "password":
        st.session_state['role'] = 'admin'
        return True
    elif username == "user" and password == "password":
        st.session_state['role'] = 'user'
        return True
    else:
        return False

def display_logs(conn):
    st.subheader("All Logs")
    all_rows = get_all_data(conn, "logs")
    if all_rows:
        for row in all_rows:
            st.write(f"ID: {row.log_id}, User ID: {row.user_id}, Username: {row.username}, Action: {row.action}, Timestamp: {row.timestamp}")
    else:
        st.info("No logs found.")

# Function to display all users
def display_users(conn):
    st.subheader("All Users")
    all_rows = get_all_data(conn)
    if all_rows:
        for row in all_rows:
            st.write(f"ID: {row.id}, Name: {row.name}, Age: {row.age}")
    else:
        st.info("No users found.")

# Main Streamlit application
def main():
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'role' not in st.session_state:
        st.session_state['role'] = None

    # Login form
    if not st.session_state['authenticated']:
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state['authenticated'] = True
                st.session_state['username'] = username
                st.success(f"Logged in as {username}")
            else:
                st.error("Invalid username or password")

    # If authenticated, show CRUD operations
    if st.session_state['authenticated']:
        st.title("CRUD Operations")
        conn = connect_to_app_database()
        if conn:
            create_table(conn)  # Ensure the users table exists
            create_log_table(conn)  # Ensure the logs table exists
            st.sidebar.header("CRUD Operations")
            operation = st.sidebar.radio("Select Operation", ("Create", "Read", "Update", "Delete"))

            if operation == "Create":
                st.subheader("Create User")
                name = st.text_input("Name:")
                age = st.number_input("Age:", min_value=0, max_value=150, step=1)
                display_users(conn)
                if st.button("Create"):
                    if name and age:
                        insert_data(conn, st.session_state['username'], name, age)

            elif operation == "Read":
                st.subheader("View Users")
                display_users(conn)

            elif operation == "Update":
                st.subheader("Update User")
                user_id = st.number_input("Enter User ID to update:", min_value=1, step=1)
                name = st.text_input("New Name:")
                age = st.number_input("New Age:", min_value=0, max_value=150, step=1)
                display_users(conn)
                if st.button("Update"):
                    if user_id and name and age:
                        update_data(conn, st.session_state['username'], user_id, name, age)

            elif operation == "Delete":
                st.subheader("Delete User")
                user_id = st.number_input("Enter User ID to delete:", min_value=1, step=1)
                display_users(conn)
                if st.button("Delete"):
                    if user_id:
                        delete_data(conn, st.session_state['username'], user_id)

            if st.session_state['role'] == 'admin':
                st.sidebar.header("Admin Operations")
                if st.sidebar.button("View Logs"):
                    display_logs(conn)
        else:
            st.error("Failed to connect to the database")

if __name__ == "__main__":
    main()
