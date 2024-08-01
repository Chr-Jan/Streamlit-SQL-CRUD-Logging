import pyodbc
import pandas as pd
import streamlit as st

from core.connection import connect_to_app_database
from core.logging import log_action

def get_all_food_data(conn, table="food"):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        return rows
    except pyodbc.Error as e:
        st.error(f"Error retrieving data: {e}")
        return None

def get_food_production_data(conn):
    try:
        query = "SELECT * FROM dbo.food_production"
        df = pd.read_sql(query, conn)
        return df
    except pyodbc.Error as e:
        st.error(f"Error fetching data from 'food_production' table: {e}")
        return None

def insert_food_production(conn, food_name, production_date, quantity, goal_reacted):
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO dbo.food_production (food_name, production_date, quantity, goal_reacted)
            VALUES (?, ?, ?, ?)
            """,
            (food_name, production_date, quantity, goal_reacted)
        )
        conn.commit()
        st.success("Record inserted successfully.")
    except pyodbc.Error as e:
        st.error(f"Error inserting record into 'food_production' table: {e}")

def delete_food_data(conn, username, production_id):
    try:
        cursor = conn.cursor()

        # Check if the food item exists
        cursor.execute("SELECT COUNT(*) FROM dbo.food_production WHERE production_id = ?", (production_id,))
        if cursor.fetchone()[0] == 0:
            st.error(f"Food item with ID {production_id} does not exist.")
            return
               
        # Delete the food item
        cursor.execute("DELETE FROM dbo.food_production WHERE production_id = ?", (production_id,))
        conn.commit()
        st.success(f"Deleted food item with ID {production_id} from 'food_production' table")
        log_action(username, production_id, f"Deleted food item with ID {production_id}")
    except pyodbc.Error as e:
        st.error(f"Error deleting data: {e}")