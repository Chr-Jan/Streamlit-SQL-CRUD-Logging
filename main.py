import pyodbc
import streamlit as st

# Function to establish connection to MS SQL Server
def connect_to_database():
    try:
        conn = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=your_server_name;"  # Replace with your server name
            "Database=your_database_name;"  # Replace with your database name
            "Trusted_Connection=yes;"
        )
        return conn
    except pyodbc.Error as e:
        st.error(f"Error connecting to MS SQL Server: {e}")
        return None

# Function to create table if it doesn't exist
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT PRIMARY KEY,
                name VARCHAR(50),
                age INT
            )
        """)
        conn.commit()
    except pyodbc.Error as e:
        st.error(f"Error creating table: {e}")

# Function to insert data into 'users' table
def insert_data(conn, name, age):
    try:
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO users (name, age) VALUES ('{name}', {age})")
        conn.commit()
        st.success(f"Inserted '{name}' with age {age} into 'users' table")
    except pyodbc.Error as e:
        st.error(f"Error inserting data: {e}")

# Function to retrieve all data from 'users' table
def get_all_data(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows
    except pyodbc.Error as e:
        st.error(f"Error retrieving data: {e}")
        return None

# Function to update data in 'users' table
def update_data(conn, user_id, name, age):
    try:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET name = '{name}', age = {age} WHERE id = {user_id}")
        conn.commit()
        st.success(f"Updated user with ID {user_id} in 'users' table")
    except pyodbc.Error as e:
        st.error(f"Error updating data: {e}")

# Function to delete data from 'users' table
def delete_data(conn, user_id):
    try:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM users WHERE id = {user_id}")
        conn.commit()
        st.success(f"Deleted user with ID {user_id} from 'users' table")
    except pyodbc.Error as e:
        st.error(f"Error deleting data: {e}")

# Main Streamlit application
def main():
    # Initialize session state
    if 'conn' not in st.session_state:
        st.session_state['conn'] = connect_to_database()

    # Set page configuration
    st.set_page_config(page_title="CRUD Operations with Streamlit", layout="wide")

    conn = st.session_state['conn']

    if conn:
        st.sidebar.header("CRUD Operations")
        operation = st.sidebar.radio("Select Operation", ("Create", "Read", "Update", "Delete"))

        if operation == "Create":
            st.subheader("Create User")
            name = st.text_input("Name:")
            age = st.number_input("Age:", min_value=0, max_value=150, step=1)
            if st.button("Create"):
                if name and age:
                    insert_data(conn, name, age)

        elif operation == "Read":
            st.subheader("View Users")
            rows = get_all_data(conn)
            if rows:
                for row in rows:
                    st.write(f"ID: {row.id}, Name: {row.name}, Age: {row.age}")
            else:
                st.info("No users found.")

        elif operation == "Update":
            st.subheader("Update User")
            user_id = st.number_input("Enter User ID to update:", min_value=1, step=1)
            name = st.text_input("New Name:")
            age = st.number_input("New Age:", min_value=0, max_value=150, step=1)
            if st.button("Update"):
                if user_id and name and age:
                    update_data(conn, user_id, name, age)

            # Display all users after update
            st.subheader("All Users")
            all_rows = get_all_data(conn)
            if all_rows:
                for row in all_rows:
                    st.write(f"ID: {row.id}, Name: {row.name}, Age: {row.age}")

        elif operation == "Delete":
            st.subheader("Delete User")
            user_id = st.number_input("Enter User ID to delete:", min_value=1, step=1)
            if st.button("Delete"):
                if user_id:
                    delete_data(conn, user_id)

    # Note: Do not close connection here to avoid premature closure

if __name__ == "__main__":
    main()
