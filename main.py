import streamlit as st
from database.connection import connect_to_database
from database.init_db import create_table
from database.crud import insert_data, get_all_data, update_data, delete_data

def main():
    # Initialize session state
    if 'conn' not in st.session_state:
        st.session_state['conn'] = connect_to_database()
    
    conn = st.session_state['conn']

    if conn:
        create_table(conn)  # Ensure the table exists
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
