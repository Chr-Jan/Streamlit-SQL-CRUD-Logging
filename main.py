import pyodbc
import streamlit as st
from time import sleep
from database.connection import connect_to_app_database
from database.init_db import create_people_table, create_log_table, create_user_table, create_roles_table, insert_default_roles, insert_default_users
from database.crud import get_all_data, insert_data, update_data, delete_data

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


def display_logs(conn):
    st.subheader("All Logs")
    all_rows = get_all_data(conn, "logs")
    if all_rows:
        for row in all_rows:
            st.write(f"ID: {row.log_id}, User ID: {row.user_id}, Username: {row.username}, Action: {row.action}, Timestamp: {row.timestamp}")
    else:
        st.info("No logs found.")

def user_db(conn):
    st.subheader("Users")
    if conn:
        try:
            all_rows = get_all_data(conn, "users")
            if all_rows:
                for row in all_rows:
                    # Fetch role name based on role_id
                    role_cursor = conn.cursor()
                    # Query to fetch the role name based on the role_id in the current row
                    role_cursor.execute("SELECT role_name FROM roles WHERE role_id = ?", (row.role_id,))
                    # Fetch the result of the query; get the first element from the tuple (role_name)                    
                    role_name = role_cursor.fetchone()[0]
                    
                    st.write(f"ID: {row.user_id}, Username: {row.username}, Password: {row.password}, Role: {role_name}")
            else:
                st.info("No users found.")
        except Exception as e:
            st.error(f"Error retrieving users data: {e}")
        finally:
            conn.close()
    else:
        st.error("Failed to connect to the database.")



def display_people(conn):
    st.subheader("All Users")
    all_rows = get_all_data(conn, "people")
    if all_rows:
        for row in all_rows:
            st.write(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Age + 2: {row[3]},")
    else:
        st.info("No users found.")

def logout():
    st.session_state['authenticated'] = False
    st.session_state['username'] = None
    st.session_state['role'] = None
    st.info("Logged out successfully!")
    sleep(0.5)
    st.experimental_rerun()

def show_temp_message(message, duration=3):
    """Show a temporary message that disappears after a given duration."""
    with st.empty():
        st.success(message)
        sleep(duration)

def main():

    conn = connect_to_app_database()

    # Check if initialization has already been performed
    if 'initialized' not in st.session_state or not st.session_state['initialized']:
        if conn:
            create_people_table(conn)
            create_log_table(conn)
            create_user_table(conn)
            create_roles_table(conn)
            insert_default_roles(conn)
            insert_default_users(conn)
            st.session_state['initialized'] = True
        else:
            print("Failed to connect to one or more databases.")
            return  # Exit early if initialization fails


    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'role' not in st.session_state:
        st.session_state['role'] = None

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

    if st.session_state['authenticated']:
        st.title("CRUD Operations")
        conn = connect_to_app_database()
        if conn:
            st.sidebar.header("CRUD Operations")
            operation = st.sidebar.radio("Select Operation", ("Create", "Read", "Update", "Delete"))

            if operation == "Create":
                st.subheader("Create User")
                name = st.text_input("Name:")
                age = st.number_input("Age:", min_value=0, max_value=150, step=1)
                display_people(conn)
                if st.button("Create"):
                    if name and age:
                        insert_data(conn, st.session_state['username'], name, age)

            elif operation == "Read":
                st.subheader("View Users")
                display_people(conn)

            elif operation == "Update":
                st.subheader("Update User")
                user_id = st.number_input("Enter User ID to update:", min_value=1, step=1)
                name = st.text_input("New Name:")
                age = st.number_input("New Age:", min_value=0, max_value=150, step=1)
                display_people(conn)
                if st.button("Update"):
                    if user_id and name and age:
                        update_data(conn, st.session_state['username'], user_id, name, age)

            elif operation == "Delete":
                st.subheader("Delete User")
                user_id = st.number_input("Enter User ID to delete:", min_value=1, step=1)
                display_people(conn)
                if st.button("Delete"):
                    if user_id:
                        delete_data(conn, st.session_state['username'], user_id)

            if st.sidebar.button("Logout"):
                logout()

            if st.session_state['role'] == 'admin':
                st.sidebar.header("Admin Operations")
                if st.sidebar.button("View Logs"):
                    display_logs(conn)
                if st.sidebar.button("Users"):
                    user_db(conn)
        else:
            st.error("Failed to connect to the database")

if __name__ == "__main__":
    main()
