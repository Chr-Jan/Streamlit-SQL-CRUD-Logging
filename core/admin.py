import pyodbc
import streamlit as st
from core.connection import connect_to_app_database
from core.crud_people import get_all_data_people

def user_db(conn):
    st.subheader("Users")
    if conn:
        try:
            all_rows = get_all_data_people(conn, "users")
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

def display_log_people(conn):
    st.subheader("All Logs")
    all_rows = get_all_data_people(conn, "log_people")
    if all_rows:
        for row in all_rows:
            st.write(f"ID: {row.log_id}, User ID: {row.user_id}, Username: {row.username}, Action: {row.action}, Timestamp: {row.timestamp}")
    else:
        st.info("No logs found.")


