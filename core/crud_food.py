import pyodbc
import pandas as pd
import streamlit as st
from core.connection import connect_to_app_database

def get_all_food_data(conn, table="food"):

    conn = connect_to_app_database

    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        return rows
    except pyodbc.Error as e:
        st.error(f"Error retrieving data {e}")
        return None

def get_food_production_data(conn):
    try:
        query = "SELECT * FROM dbo.food_production"
        df = pd.read_sql(query, conn)
        return df
    except pyodbc.Error as e:
        print(f"Error fetching data from 'food_production' table: {e}")
        return None

def insert_food_production(conn, food_name, production_date, quantity):

    conn = connect_to_app_database

    try:
        cursor = conn.cursor()
        goal_reacted = 1 if quantity > 10 else 0
        cursor.execute(
            """
            INSERT INTO dbo.food_production (food_name, production_date, quantity, goal_reacted)
            VALUES (?, ?, ?, ?)
            """,
            (food_name, production_date, quantity, goal_reacted)
        )
        conn.commit()
        print("Record inserted successfully.")
    except pyodbc.Error as e:
        print(f"Error inserting record into 'food_production' table: {e}")
