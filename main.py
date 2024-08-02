import pyodbc
import streamlit as st
from time import sleep
from core.connection import connect_to_app_database
from core.init_db import create_people_table, create_log_people_table, create_user_table, create_roles_table, insert_default_roles, insert_default_users, create_food_production_table, seed_food_production_table
from core.crud_people import get_all_data_people, insert_data, update_data, delete_data
from core.crud_food import get_food_production_data, insert_food_production, delete_food_data, update_food_data
from core.admin import user_db, display_log_people
from core.auth import authenticate, register_user

def display_people(conn):
    st.subheader("All Users")
    all_rows = get_all_data_people(conn, "people")
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
    st.rerun()

def show_temp_message(message, duration=3):
    """Show a temporary message that disappears after a given duration."""
    with st.empty():
        st.success(message)
        sleep(duration)

# Registration function
def register_user(conn, username, password, role_name):
    try:
        cursor = conn.cursor()

        # Check if the username already exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
        if cursor.fetchone()[0] > 0:
            st.error("Username already exists.")
            return

        # Retrieve the role ID for the given role name
        cursor.execute("SELECT role_id FROM roles WHERE role_name = ?", (role_name,))
        role_id = cursor.fetchone()[0]

        # Insert the new user into the users table
        cursor.execute("INSERT INTO users (username, password, role_id) VALUES (?, ?, ?)",
                       (username, password, role_id))
        conn.commit()
        st.success(f"Registered new user: {username}")

    except pyodbc.Error as e:
        st.error(f"Error registering user: {e}")

def main():
    conn = connect_to_app_database()

    # Check if initialization has already been performed
    if 'initialized' not in st.session_state or not st.session_state['initialized']:
        if conn:
            create_roles_table(conn)
            create_user_table(conn)
            create_people_table(conn)
            create_food_production_table(conn)
            create_log_people_table(conn)
            insert_default_roles(conn)
            insert_default_users(conn)
            seed_food_production_table(conn)
            st.session_state['initialized'] = True
        else:
            st.error("Failed to connect to the database.")
            return  # Exit early if initialization fails

    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'role' not in st.session_state:
        st.session_state['role'] = None

    if not st.session_state['authenticated']:
        st.title("User Registration / Login")
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state['authenticated'] = True
                st.session_state['username'] = username
                st.success(f"Logged in as {username}")
                st.rerun()
            else:
                st.error("Invalid username or password")

        st.subheader("Register New User")
        reg_username = st.text_input("New Username")
        reg_password = st.text_input("New Password", type="password")
        reg_role = st.selectbox("Role", ["user", "admin"])
        if st.button("Register"):
            if reg_username and reg_password and reg_role:
                if conn:
                    register_user(conn, reg_username, reg_password, reg_role)
                else:
                    st.error("Failed to connect to the database.")

    if st.session_state['authenticated']:
        st.title("Data:")
        if conn:
            main_operation = st.sidebar.selectbox("Select Operation", 
                ("People Operations", "Food Operations", "Admin Operations"))

            if main_operation == "People Operations":
                st.sidebar.header("People Operations")
                people_operation = st.sidebar.selectbox("Select People Operation", 
                    ("Create", "Read", "Update", "Delete"))

                if people_operation == "Create":
                    st.subheader("Create User")
                    name = st.text_input("Name:")
                    age = st.number_input("Age:", min_value=0, max_value=150, step=1)
                    display_people(conn)
                    if st.button("Create"):
                        if name and age:
                            insert_data(conn, st.session_state['username'], name, age)

                elif people_operation == "Read":
                    st.subheader("View Users")
                    display_people(conn)

                elif people_operation == "Update":
                    st.subheader("Update User")
                    user_id = st.number_input("Enter User ID to update:", min_value=1, step=1)
                    name = st.text_input("New Name:")
                    age = st.number_input("New Age:", min_value=0, max_value=150, step=1)
                    display_people(conn)
                    if st.button("Update"):
                        if user_id and name and age:
                            update_data(conn, st.session_state['username'], user_id, name, age)

                elif people_operation == "Delete":
                    st.subheader("Delete User")
                    user_id = st.number_input("Enter User ID to delete:", min_value=1, step=1)
                    display_people(conn)
                    if st.button("Delete"):
                        if user_id:
                            delete_data(conn, st.session_state['username'], user_id)

            elif main_operation == "Food Operations":
                st.sidebar.header("Food Operations")
                food_operation = st.sidebar.selectbox("Select Food Operation", 
                    ("View Food", "Insert Data", "Delete", "Update"))

                if food_operation == "View Food":
                    st.subheader("View Food Information")
                    df = get_food_production_data(conn)
                    if df is not None:
                        st.dataframe(df)
                    else:
                        st.error("Failed to fetch food production data.")
                
                elif food_operation == "Insert Data":
                    st.subheader("Create food insertion information")
                    food_name = st.text_input("Food Name:")
                    production_date = st.date_input("Day of production:")
                    quantity = st.number_input(f"Amount of {food_name} made:")
                    st.write("0 = no, 1 = yes")
                    goal_reacted = st.number_input("Goal reached:", min_value=0, max_value=1, step=1)
                    if st.button("Create"):
                        if food_name and production_date and quantity and goal_reacted is not None:
                            insert_food_production(conn, food_name, production_date, quantity, goal_reacted)
                    
                    df = get_food_production_data(conn)
                    if df is not None:
                        st.dataframe(df)
                    else:
                        st.error("Failed to fetch food production data.")
                
                elif food_operation == "Update":
                    st.subheader("Update Food Information")
                    production_id = st.number_input("Enter Food Item ID to update:", min_value=1, step=1)
                    food_name = st.text_input("New Name:")
                    production_date = st.date_input("New Production Date:")
                    quantity = st.number_input(f"New amount of {food_name} made:")
                    st.write("0 = no, 1 = yes")
                    goal_reacted = st.number_input("New Goal reached:", min_value=0, max_value=1, step=1)

                    df = get_food_production_data(conn)
                    if df is not None:
                        st.dataframe(df)
                    else:
                        st.error("Failed to fetch food production data.")

                    if st.button("Update"):
                        if production_id and food_name and production_date and quantity and goal_reacted is not None:
                            update_food_data(conn, st.session_state['username'], production_id, food_name, production_date, quantity, goal_reacted)

                elif food_operation == "Delete":
                    st.subheader("Delete Food Information")
                    production_id = st.number_input("Enter Food Item ID to delete:", min_value=1, step=1)
                    get_food_production_data(conn)
                    if st.button("Delete"):
                        if production_id: 
                            delete_food_data(conn, st.session_state['username'], production_id)

                    df = get_food_production_data(conn)
                    if df is not None:
                        st.dataframe(df)
                    else:
                        st.error("Failed to fetch food production data.")

            elif main_operation == "Admin Operations":
                if st.session_state['role'] == 'admin':
                    st.sidebar.header("Admin Operations")
                    admin_operation = st.sidebar.selectbox("Select Admin Operation", 
                        ("View Logs", "Manage Users"))

                    if admin_operation == "View Logs":
                        st.subheader("View Logs")
                        display_log_people(conn)
                    
                    elif admin_operation == "Manage Users":
                        st.subheader("Manage Users")
                        user_db(conn)
                else:
                    st.error("You do not have permission to access admin operations.")

            if st.sidebar.button("Logout"):
                logout()

        else:
            st.error("Failed to connect to the database")

if __name__ == "__main__":
    main()
